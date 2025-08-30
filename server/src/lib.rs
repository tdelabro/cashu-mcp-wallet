use std::{convert::Infallible, str::FromStr, sync::Arc};

use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use rmcp::{
    ErrorData, ServerHandler,
    handler::server::router::tool::ToolRouter,
    model::{CallToolResult, ServerCapabilities, ServerInfo},
    schemars, serde_json, tool, tool_handler, tool_router,
};
use starknet_types::Unit as StarknetUnit;
use wallet::db::balance::GetForAllNodesData;

#[derive(Debug, serde::Serialize, schemars::JsonSchema)]
#[schemars(
    title = "Mint Balances",
    description = "Complete balance information for a Cashu mint, including all available token denominations"
)]
pub struct MintBalances {
    #[schemars(
        url,
        description = "Base URL of the Cashu mint server",
        example = "https://mint.example.com"
    )]
    pub url: String,
    #[schemars(
        description = "Array containing balance information for each token unit available at this mint"
    )]
    pub balances: Vec<Balance>,
}

#[derive(Debug, serde::Serialize, schemars::JsonSchema)]
#[schemars(
    title = "Token Balance",
    description = "Balance information for a specific asset"
)]
pub struct Balance {
    #[schemars(description = "Token unit identifier", example = &"sat")]
    pub unit: Unit,
    #[schemars(
        description = "Total amount of tokens held in this unit.",
        example = "50000",
        range(min = 1)
    )]
    pub amount: u64,
}

#[derive(Debug, serde::Serialize, schemars::JsonSchema)]
#[schemars(
    description = "Supported token units in Cashu. For each one you have the base token their represent as well as the conversion rate."
)]
pub enum Unit {
    #[schemars(
        description = "A milli strk",
        extend("conversion_rate" = "10^-6", "base_token" = "STRK")
    )]
    MilliStrk,
    #[schemars(
        description = "A gwei",
        extend("conversion_rate" = "10^-9", "base_token" = "ETH")
    )]
    Gwei,
    #[schemars(
        description = "A sat",
        extend("conversion_rate" = "10^-8", "base_token" = "WBTC")
    )]
    Satoshi,
    #[schemars(
        description = "A micro USDT",
        extend("conversion_rate" = "10^-6", "base_token" = "USDT")
    )]
    MicroUsdT,
    #[schemars(
        description = "A micro USDC",
        extend("conversion_rate" = "10^-6", "base_token" = "USDC")
    )]
    MicroUsdC,
    #[schemars(
        description = "An asset that wasn't preconfigured. We have no information about its value."
    )]
    Other(String),
}

impl FromStr for Unit {
    type Err = Infallible;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let x = match s {
            val if val == StarknetUnit::MilliStrk.as_str() => Unit::MilliStrk,
            val if val == StarknetUnit::Gwei.as_str() => Unit::Gwei,
            val if val == StarknetUnit::Satoshi.as_str() => Unit::Satoshi,
            val if val == StarknetUnit::MicroUsdT.as_str() => Unit::MicroUsdT,
            val if val == StarknetUnit::MicroUsdC.as_str() => Unit::MicroUsdC,
            val => Unit::Other(val.to_string()),
        };

        Ok(x)
    }
}

pub trait DataService: Send + Sync + 'static {
    type Error: std::error::Error + Send + Sync + 'static + Into<ErrorData>;

    fn balance(&self) -> Result<Vec<GetForAllNodesData>, Self::Error>;
}

impl From<DataServiceError> for ErrorData {
    fn from(error: DataServiceError) -> Self {
        match error {
            DataServiceError::Pool(e) => ErrorData::internal_error(
                "failed to get a database connection from the pool",
                Some(serde_json::to_value(e.to_string()).unwrap()),
            ),
            DataServiceError::Db(e) => ErrorData::internal_error(
                "failed to interact with the database",
                Some(serde_json::to_value(e.to_string()).unwrap()),
            ),
        }
    }
}

#[derive(Debug, Clone)]
pub struct MemoryDataService {
    pool: Pool<SqliteConnectionManager>,
}

impl MemoryDataService {
    pub fn new(pool: Pool<SqliteConnectionManager>) -> Self {
        Self { pool }
    }
}

#[derive(Debug, thiserror::Error)]
pub enum DataServiceError {
    #[error(transparent)]
    Pool(#[from] r2d2::Error),
    #[error(transparent)]
    Db(#[from] rusqlite::Error),
}

impl DataService for MemoryDataService {
    type Error = DataServiceError;

    fn balance(&self) -> Result<Vec<GetForAllNodesData>, DataServiceError> {
        let conn = self.pool.get()?;
        let balances = wallet::db::balance::get_for_all_nodes(&conn)?;
        Ok(balances)
    }
}

#[derive(Debug, Clone)]
pub struct GenericService<DS: DataService> {
    #[allow(dead_code)]
    data_service: Arc<DS>,
    tool_router: ToolRouter<Self>,
}

#[derive(Debug, schemars::JsonSchema, serde::Deserialize, serde::Serialize)]
pub struct SetDataRequest {
    pub data: String,
}

#[tool_router]
impl<DS: DataService> GenericService<DS> {
    pub fn new(data_service: DS) -> Self {
        Self {
            data_service: Arc::new(data_service),
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
        let balances: Vec<_> = self
            .data_service
            .balance()
            .map_err(|e| e.into())?
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

        Ok(CallToolResult::structured(
            serde_json::to_value(balances).unwrap(),
        ))
    }
}

#[tool_handler]
impl<DS: DataService> ServerHandler for GenericService<DS> {
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
