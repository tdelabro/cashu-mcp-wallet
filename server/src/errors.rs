use rmcp::{ErrorData, serde_json};

#[derive(Debug, thiserror::Error)]
pub enum CashuWalletServiceError {
    #[error(transparent)]
    Pool(#[from] r2d2::Error),
    #[error(transparent)]
    Db(#[from] rusqlite::Error),
    #[error(transparent)]
    CompactWadFromStr(#[from] wallet::types::compact_wad::Error),
    #[error(transparent)]
    SeedPhrase(#[from] wallet::wallet::sqlite::Error),
    #[error(transparent)]
    ConnectToNode(#[from] wallet::ConnectToNodeError),
    #[error(transparent)]
    Register(#[from] wallet::node::RegisterNodeError),
    #[error(transparent)]
    ReceiveWad(#[from] wallet::errors::Error),
    #[error(transparent)]
    ParseAssetAmount(#[from] parse_asset_amount::ParseAmountStringError),
    #[error(transparent)]
    PlanSpending(#[from] wallet::send::PlanSpendingError),
    #[error("not enought funds in node {0}")]
    NotEnoughFunds(u32),
}

impl From<CashuWalletServiceError> for ErrorData {
    fn from(error: CashuWalletServiceError) -> Self {
        match error {
            CashuWalletServiceError::Pool(error) => ErrorData::internal_error(
                "failed to get a database connection from the pool",
                Some(serde_json::to_value(error.to_string()).unwrap()),
            ),
            CashuWalletServiceError::Db(error) => ErrorData::internal_error(
                "failed to interact with the database",
                Some(serde_json::to_value(error.to_string()).unwrap()),
            ),
            CashuWalletServiceError::CompactWadFromStr(error) => ErrorData::invalid_params(
                "invalid value for wads parameter",
                Some(serde_json::to_value(error.to_string()).unwrap()),
            ),
            CashuWalletServiceError::SeedPhrase(error) => ErrorData::internal_error(
                "failed to retreive the wallet seed phrase",
                Some(serde_json::to_value(error.to_string()).unwrap()),
            ),
            CashuWalletServiceError::ConnectToNode(connect_to_node_error) => {
                ErrorData::internal_error(
                    "failed to connect to the mint node",
                    Some(serde_json::to_value(connect_to_node_error.to_string()).unwrap()),
                )
            }
            CashuWalletServiceError::Register(register_node_error) => ErrorData::internal_error(
                "failed to register the mint node",
                Some(serde_json::to_value(register_node_error.to_string()).unwrap()),
            ),
            CashuWalletServiceError::ReceiveWad(error) => ErrorData::internal_error(
                "failed to receive a wad",
                Some(serde_json::to_value(error.to_string()).unwrap()),
            ),
            CashuWalletServiceError::ParseAssetAmount(parse_amount_string_error) => {
                ErrorData::invalid_params(
                    "invalid argument amount",
                    Some(serde_json::to_value(parse_amount_string_error.to_string()).unwrap()),
                )
            }
            CashuWalletServiceError::PlanSpending(plan_spending_error) => {
                ErrorData::internal_error(
                    "could not plan spending",
                    Some(serde_json::to_value(plan_spending_error.to_string()).unwrap()),
                )
            }
            CashuWalletServiceError::NotEnoughFunds(_) => {
                ErrorData::internal_error("not enough funds", None)
            }
        }
    }
}
