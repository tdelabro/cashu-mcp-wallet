use std::sync::Arc;

use rmcp::{
    ErrorData, ServerHandler,
    handler::server::{router::tool::ToolRouter, wrapper::Parameters},
    model::{CallToolResult, ServerCapabilities, ServerInfo},
    serde_json, tool, tool_handler, tool_router,
};

use crate::{
    balances::MintBalances,
    cashu_wallet_service::CashuWalletService,
    wad::{CreateWadsRequest, CreateWadsResponse, ReceiveWadsRequest, ReceiveWadsResponse},
};

pub use cashu_wallet_service::SqliteCashuWalletService;

mod balances;
mod cashu_wallet_service;
mod errors;
mod wad;

#[derive(Debug, Clone)]
pub struct GenericService<DS: CashuWalletService> {
    #[allow(dead_code)]
    cashu_wallet_service: Arc<DS>,
    tool_router: ToolRouter<Self>,
}

#[tool_router]
impl<DS: CashuWalletService> GenericService<DS> {
    pub fn new(cashu_wallet_service: DS) -> Self {
        Self {
            cashu_wallet_service: Arc::new(cashu_wallet_service),
            tool_router: Self::tool_router(),
        }
    }

    #[tool(
        description = r#"Retrieves the current balance of ecash tokens across all recorded Cashu mints. Each mint returns its available token amounts grouped by currency unit (e.g., MicroUsdC, Satoshi, Gwei).
Useful for checking spendable funds before transactions, as this is the money available to be spent at the moment.
Any mint or asset not present in the list has a balance of 0."#,
        annotations(
            read_only_hint = true,
            destructive_hint = false,
            idempotent_hint = true,
            open_world_hint = false,
        ),
        output_schema = rmcp::handler::server::tool::cached_schema_for_type::<MintBalances>(),
    )]
    pub async fn get_all_nodes_balances(&self) -> Result<CallToolResult, ErrorData> {
        let balances = self.cashu_wallet_service.balance().map_err(|e| e.into())?;

        Ok(CallToolResult::structured(
            serde_json::to_value(balances).unwrap(),
        ))
    }

    #[tool(
        description = "Receive money. Use this tool to store the tokens of the wads you received in your wallet.
It will swap the cashu tokens for new ones, only know by this wallet, preventing double spend and finalizing the transfer flow.",
        annotations(
            read_only_hint = false,
            destructive_hint = false,
            idempotent_hint = false,
            open_world_hint = false,
        ),
        output_schema = rmcp::handler::server::tool::cached_schema_for_type::<ReceiveWadsResponse>(),
    )]
    pub async fn receive_wads(
        &self,
        Parameters(ReceiveWadsRequest { wads }): Parameters<ReceiveWadsRequest>,
    ) -> Result<CallToolResult, ErrorData> {
        let receipts = self
            .cashu_wallet_service
            .receive_wads(wads)
            .await
            .map_err(|e| e.into())?;

        Ok(CallToolResult::structured(
            serde_json::to_value(ReceiveWadsResponse {
                wads_received: receipts,
            })
            .unwrap(),
        ))
    }

    #[tool(
        description = "Create wads from the wallet tokens. It will take money out of the wallet to put it into the wads.
It can use money from multiple mints, therfore creating multiples wads. The wallet balance will be decreased from the same amount as the tokens extracted.
The returned coma separated wads string should be used to send money to other users. It can also be received by the same wallet, to recover the funds contained in the wads.
",
        annotations(
            read_only_hint = false,
            destructive_hint = false,
            idempotent_hint = false,
            open_world_hint = false,
        ),
        output_schema = rmcp::handler::server::tool::cached_schema_for_type::<CreateWadsResponse>(),
    )]
    pub async fn create_wads(
        &self,
        Parameters(CreateWadsRequest { amount, asset }): Parameters<CreateWadsRequest>,
    ) -> Result<CallToolResult, ErrorData> {
        let wads = self
            .cashu_wallet_service
            .create_wads(amount, asset.to_string())
            .await
            .map_err(|e| e.into())?;

        Ok(CallToolResult::structured(
            serde_json::to_value(CreateWadsResponse { wads }).unwrap(),
        ))
    }
}

#[tool_handler]
impl<DS: CashuWalletService> ServerHandler for GenericService<DS> {
    fn get_info(&self) -> ServerInfo {
        ServerInfo {
            instructions: Some(
                r#"A cashu wallet.
It can be used to interact with the cashu protocol.
This implementation extend the protocol beyond just Bitcoin and support other chains, starting with Starknet.
Use it to consult balances and load tokens from storage in order to transfer them."#
                    .into(),
            ),
            capabilities: ServerCapabilities::builder().enable_tools().build(),
            ..Default::default()
        }
    }
}
