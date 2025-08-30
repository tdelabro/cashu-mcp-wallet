use std::str::FromStr;

use parse_asset_amount::parse_asset_amount;
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use rmcp::ErrorData;
use starknet_types::Asset;
use tracing::{Level, event};
use wallet::types::compact_wad::{CompactWad, CompactWads};

use crate::{
    balances::{Balance, MintBalances, Unit},
    errors::CashuWalletServiceError,
    wad::WadReceptionInfo,
};

#[async_trait::async_trait]
pub trait CashuWalletService: Send + Sync + 'static {
    type Error: std::error::Error + Send + Sync + 'static + Into<ErrorData>;

    fn balance(&self) -> Result<Vec<MintBalances>, Self::Error>;
    async fn receive_wads(&self, wad_string: String) -> Result<Vec<WadReceptionInfo>, Self::Error>;
    async fn create_wads(&self, amount: String, asset: String) -> Result<String, Self::Error>;
}

#[derive(Debug, Clone)]
pub struct SqliteCashuWalletService {
    db_pool: Pool<SqliteConnectionManager>,
}

impl SqliteCashuWalletService {
    pub fn new(pool: Pool<SqliteConnectionManager>) -> Self {
        Self { db_pool: pool }
    }
}

#[async_trait::async_trait]
impl CashuWalletService for SqliteCashuWalletService {
    type Error = CashuWalletServiceError;

    fn balance(&self) -> Result<Vec<MintBalances>, CashuWalletServiceError> {
        let conn = self.db_pool.get()?;
        let balances = wallet::db::balance::get_for_all_nodes(&conn)?
            .into_iter()
            .map(|b| MintBalances {
                url: b.url.to_string(),
                balances: b
                    .balances
                    .into_iter()
                    .map(|b| Balance {
                        unit: Unit::from_str(&b.unit).unwrap(),
                        amount: b.amount.into(),
                    })
                    .collect(),
            })
            .collect();

        Ok(balances)
    }

    async fn receive_wads(
        &self,
        wad_string: String,
    ) -> Result<Vec<WadReceptionInfo>, CashuWalletServiceError> {
        let wads: CompactWads<starknet_types::Unit> = wad_string.parse()?;
        let seed_phrase_manager =
            wallet::wallet::sqlite::SeedPhraseManager::new(self.db_pool.clone())?;

        let mut receipts = Vec::with_capacity(wads.0.len());

        for wad in wads.0 {
            let mut node_client = wallet::connect_to_node(&wad.node_url, None).await?;
            let node_id =
                wallet::node::register(self.db_pool.clone(), &mut node_client, &wad.node_url)
                    .await?;
            let CompactWad {
                node_url,
                unit,
                memo,
                proofs,
            } = wad;

            let received_amount = wallet::receive_wad(
                seed_phrase_manager.clone(),
                self.db_pool.clone(),
                &mut node_client,
                node_id,
                &node_url,
                unit.as_str(),
                proofs,
                &memo,
            )
            .await?;
            event!(name: "wad-received", Level::INFO, mint_url = %node_url, amount = %received_amount, %unit);

            receipts.push(WadReceptionInfo {
                mint_url: node_url.to_string(),
                amount: received_amount.into(),
                unit: Unit::from_str(unit.as_str()).unwrap(),
                memo,
            });
        }

        Ok(receipts)
    }

    async fn create_wads(
        &self,
        asset_amount: String,
        asset_string: String,
    ) -> Result<String, Self::Error> {
        let asset = Asset::from_str(&asset_string).unwrap();
        let unit = asset.find_best_unit();
        let amount = parse_asset_amount(&asset_amount, asset, unit)?;

        let db_conn = self.db_pool.get()?;
        let amount_to_use_per_node = wallet::send::plan_spending(&db_conn, amount, unit, &[])?;

        let mut wads = Vec::with_capacity(amount_to_use_per_node.len());
        let mut ys_per_node = Vec::with_capacity(amount_to_use_per_node.len());
        for (node_id, amount_to_use) in amount_to_use_per_node {
            let node_url = wallet::db::node::get_url_by_id(&db_conn, node_id)?
                .expect("ids come form DB, there should be an url");
            let mut node_client = wallet::connect_to_node(&node_url, None).await?;

            let seed_phrase_manager =
                wallet::wallet::sqlite::SeedPhraseManager::new(self.db_pool.clone())?;

            let proofs_ids = wallet::fetch_inputs_ids_from_db_or_node(
                seed_phrase_manager,
                self.db_pool.clone(),
                &mut node_client,
                node_id,
                amount_to_use,
                unit.as_str(),
            )
            .await?
            .ok_or(Self::Error::NotEnoughFunds(node_id))?;

            let db_conn = self.db_pool.get()?;
            let proofs = wallet::load_tokens_from_db(&db_conn, &proofs_ids)?;
            let wad = wallet::wad::create_from_parts(node_url, unit, None, proofs);
            wads.push(wad);
            ys_per_node.push(proofs_ids);
        }
        let db_conn = self.db_pool.get()?;
        for (wad, ys) in wads.iter().zip(ys_per_node) {
            wallet::db::wad::register_wad(
                &db_conn,
                wallet::db::wad::WadType::OUT,
                &wad.node_url,
                &wad.memo,
                &ys,
            )?;
        }

        Ok(CompactWads::new(wads).to_string())
    }
}
