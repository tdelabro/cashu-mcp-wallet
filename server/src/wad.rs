use crate::balances::Unit;

#[derive(Debug, serde::Deserialize, schemars::JsonSchema)]
#[schemars(description = "The wads we want to receive (swap for new ones with the mint).")]
pub struct ReceiveWadsRequest {
    #[schemars(
        with = "String",
        description = r#"Colon separated wads (tokenv4).
Each individual wad contain one or many tokens belonging to a single mint node.
Each individual is build with a "cashuB" prefix followed by the base64 encoding of a cbor serialized array of tokens.
Eg. "cashuB<token1>:cashuB<token2>:cashuB<token3>", where each cashuB<token> is a complete, valid single-mint wad.
Note: The online cashu specs call use the word token for both a wad and the individual power of 2 piece of amount it contains. We prefer to use the word "wad" instead to design a set of tokens belonging to the same mint and sent altogether.
"#,
        example = "cashuBgaNhbndodHRwOi8vbG9jYWxob3N0OjEwMDAzL2F1aW1pbGxpc3Rya2FwgaJhaUgAZ-dLgv8P6WFwiqNhYRkBAGFzeEA1NzhjYWVmNzEwZWVjMzFhZTBhMTQ3NmQ0ZG-gll7aUgD2f7qjYWEYIGFzeEA0ODc1MGRmMzU3OWUyN2RkZThjNjRhYjk0ZDI4ZGZlYTliOGFhZTc4YzE0MGNmMTJjODI4ODM4MTlhZWU1ZDhhYWNYIQONpTD4tUlHxpXAAkmoM7vVgF7dxi6F1sbZ6BtASucFoqNhYRkEAGFzeEBhNDI1NTMzZmI3MTQ1YzcxMTJlOWVmOTA2MmI3MmI1ZDM0ODVkZGQ0ZWQyYjY1OWEyYTg1NGZiMWQ5MmI5MjIwYWNYIQJyTPROG-OGBTU5qK-G5v5nGOks_D7YEHirVwmigVSWAaNhYRBhc3hANDhmYmY1ODQ4ZGQ4OTNiODkwMDExMTI2NDE0ZWJiNmNhY2Y1YzVhODUxMDI0YzJiZjJlZWExNjgyNzEzOGM1MWFjWCEDc2tg2XjmJe6tUsYkscGWhsJwidMAehYHbrThUvdYCUajYWEZAgBhc3hAMmFkODY1Yjk2NDJlMjBjNjU1ZWE1YWY0ZjFjMTBjZDkzZjYzMTgzMGY5NzgyZDRkMzAzZjUzOTNhYTBkMmUwM2FjWCEDoBrpwRJs_aIAdDBpqs5dYtM21ipAtYgdRAC1O95oYr6jYWEYQGFzeEBkZTkwZjUwZmMzYjExNzg3NDMxMzYzNDM2ODgyMGJlYjkzYTM1YTI2NTY2ODQ5NmUxM2Y2ZTI3ZDMxMDk5Njk4YWNYIQMYKKFNuSjtPt-j4IdOVPwgmrY9tUlioJtm38WdL5vi9KNhYRBhc3hAMzg2NjIwZjY3ODlkYWY0MzVmM2ViYzBjYjQxYzg0MjMyN2VmYjllYzhkMjk2ZTczOWU4ZmY1ZGUwMmYwZTkwMWFjWCECo34YSoyB2nW9fWL0frrD8ZnUpzjYRrHwxOs6Z5zD13c=:cashuBo2F0gqJhaUgA_9SLj17PgGFwgaNhYQFhc3hAYWNjMTI0MzVlN2I4NDg0YzNjZjE4NTAxNDkyMThhZjkwZjcxNmE1MmJmNGE1ZWQzNDdlNDhlY2MxM2Y3NzM4OGFjWCECRFODGd5IXVW-07KaZCvuWHk3WrnnpiDhHki6SCQh88-iYWlIAK0mjE0fWCZhcIKjYWECYXN4QDEzMjNkM2Q0NzA3YTU4YWQyZTIzYWRhNGU5ZjFmNDlmNWE1YjRhYzdiNzA4ZWIwZDYxZjczOGY0ODMwN2U4ZWVhY1ghAjRWqhENhLSsdHrr2Cw7AFrKUL9Ffr1XN6RBT6w659lNo2FhAWFzeEA1NmJjYmNiYjdjYzY0MDZiM2ZhNWQ1N2QyMTc0ZjRlZmY4YjQ0MDJiMTc2OTI2ZDNhNTdkM2MzZGNiYjU5ZDU3YWNYIQJzEpxXGeWZN5qXSmJjY8MzxWyvwObQGr5G1YCCgHicY2FtdWh0dHA6Ly9sb2NhbGhvc3Q6MzMzOGF1Y3NhdA=="
    )]
    pub wads: String,
}

#[derive(Debug, serde::Serialize, schemars::JsonSchema)]
pub struct ReceiveWadsResponse {
    #[schemars(description = "List of information about each wad that was received")]
    pub wads_received: Vec<WadReceptionInfo>,
}

#[derive(Debug, serde::Serialize, schemars::JsonSchema)]
#[schemars(
    description = "A wad receipt. The amount has successfully been added to the wallet balance for this mint. If you query the balances you will they have inceased."
)]
pub struct WadReceptionInfo {
    #[schemars(
        url,
        description = "Base URL of the Cashu mint server",
        example = "https://mint.example.com"
    )]
    pub mint_url: String,
    #[schemars(
        description = "The total amount of tokens received in this wad",
        example = "1000"
    )]
    pub amount: u64,
    #[schemars(description = "The unit of the received tokens")]
    pub unit: Unit,
    #[schemars(
        description = "Optional memo or note associated with the wad",
        example = "Payment for services"
    )]
    pub memo: Option<String>,
}

#[derive(Debug, serde::Deserialize, schemars::JsonSchema)]
pub struct CreateWadsRequest {
    #[schemars(
        description = "The quantity of the asset we want to spend. This should be expressed in the original asset quantity, not in `unit` quantity (which is for internal representation). It is a decimal number and, can be a float.",
        example = "42.35"
    )]
    pub amount: String,
    #[schemars(
        description = "The asset we want to spend. Original onchain asset. Not his cashu representation.",
        example = &"STRK",
        example = &"ETH",
        example = &"BTC",
        example = &"USDC",
        example = &"USDT",
    )]
    pub asset: String,
}

#[derive(Debug, serde::Serialize, schemars::JsonSchema)]
#[schemars(description = "The newly created wads. Ready to be spent.")]
pub struct CreateWadsResponse {
    #[schemars(
        with = "String",
        description = r#"Colon separated wads (tokenv4).
Each individual wad contain one or many tokens belonging to a single mint node.
Each individual is build with a "cashuB" prefix followed by the base64 encoding of a cbor serialized array of tokens.
Eg. "cashuB<token1>:cashuB<token2>:cashuB<token3>", where each cashuB<token> is a complete, valid single-mint wad.
Note: The online cashu specs call use the word token for both a wad and the individual power of 2 piece of amount it contains. We prefer to use the word "wad" instead to design a set of tokens belonging to the same mint and sent altogether.
"#,
        example = "cashuBgaNhbndodHRwOi8vbG9jYWxob3N0OjEwMDAzL2F1aW1pbGxpc3Rya2FwgaJhaUgAZ-dLgv8P6WFwiqNhYRkBAGFzeEA1NzhjYWVmNzEwZWVjMzFhZTBhMTQ3NmQ0ZG-gll7aUgD2f7qjYWEYIGFzeEA0ODc1MGRmMzU3OWUyN2RkZThjNjRhYjk0ZDI4ZGZlYTliOGFhZTc4YzE0MGNmMTJjODI4ODM4MTlhZWU1ZDhhYWNYIQONpTD4tUlHxpXAAkmoM7vVgF7dxi6F1sbZ6BtASucFoqNhYRkEAGFzeEBhNDI1NTMzZmI3MTQ1YzcxMTJlOWVmOTA2MmI3MmI1ZDM0ODVkZGQ0ZWQyYjY1OWEyYTg1NGZiMWQ5MmI5MjIwYWNYIQJyTPROG-OGBTU5qK-G5v5nGOks_D7YEHirVwmigVSWAaNhYRBhc3hANDhmYmY1ODQ4ZGQ4OTNiODkwMDExMTI2NDE0ZWJiNmNhY2Y1YzVhODUxMDI0YzJiZjJlZWExNjgyNzEzOGM1MWFjWCEDc2tg2XjmJe6tUsYkscGWhsJwidMAehYHbrThUvdYCUajYWEZAgBhc3hAMmFkODY1Yjk2NDJlMjBjNjU1ZWE1YWY0ZjFjMTBjZDkzZjYzMTgzMGY5NzgyZDRkMzAzZjUzOTNhYTBkMmUwM2FjWCEDoBrpwRJs_aIAdDBpqs5dYtM21ipAtYgdRAC1O95oYr6jYWEYQGFzeEBkZTkwZjUwZmMzYjExNzg3NDMxMzYzNDM2ODgyMGJlYjkzYTM1YTI2NTY2ODQ5NmUxM2Y2ZTI3ZDMxMDk5Njk4YWNYIQMYKKFNuSjtPt-j4IdOVPwgmrY9tUlioJtm38WdL5vi9KNhYRBhc3hAMzg2NjIwZjY3ODlkYWY0MzVmM2ViYzBjYjQxYzg0MjMyN2VmYjllYzhkMjk2ZTczOWU4ZmY1ZGUwMmYwZTkwMWFjWCECo34YSoyB2nW9fWL0frrD8ZnUpzjYRrHwxOs6Z5zD13c=:cashuBo2F0gqJhaUgA_9SLj17PgGFwgaNhYQFhc3hAYWNjMTI0MzVlN2I4NDg0YzNjZjE4NTAxNDkyMThhZjkwZjcxNmE1MmJmNGE1ZWQzNDdlNDhlY2MxM2Y3NzM4OGFjWCECRFODGd5IXVW-07KaZCvuWHk3WrnnpiDhHki6SCQh88-iYWlIAK0mjE0fWCZhcIKjYWECYXN4QDEzMjNkM2Q0NzA3YTU4YWQyZTIzYWRhNGU5ZjFmNDlmNWE1YjRhYzdiNzA4ZWIwZDYxZjczOGY0ODMwN2U4ZWVhY1ghAjRWqhENhLSsdHrr2Cw7AFrKUL9Ffr1XN6RBT6w659lNo2FhAWFzeEA1NmJjYmNiYjdjYzY0MDZiM2ZhNWQ1N2QyMTc0ZjRlZmY4YjQ0MDJiMTc2OTI2ZDNhNTdkM2MzZGNiYjU5ZDU3YWNYIQJzEpxXGeWZN5qXSmJjY8MzxWyvwObQGr5G1YCCgHicY2FtdWh0dHA6Ly9sb2NhbGhvc3Q6MzMzOGF1Y3NhdA=="
    )]
    pub wads: String,
}
