use starknet_types::Unit as StarknetUnit;

use std::{convert::Infallible, str::FromStr};

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
