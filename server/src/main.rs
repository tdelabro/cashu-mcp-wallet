use std::{path::PathBuf, str::FromStr};

use anyhow::Result;
use r2d2_sqlite::SqliteConnectionManager;
use rmcp::{ServiceExt, transport::stdio};
use tracing_subscriber::EnvFilter;

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize the tracing subscriber with file and stdout logging
    tracing_subscriber::fmt()
        .with_env_filter(EnvFilter::from_default_env().add_directive(tracing::Level::DEBUG.into()))
        .with_writer(std::io::stderr)
        .with_ansi(false)
        .init();

    tracing::info!("Starting MCP server");

    let db_path =
        PathBuf::from_str("/Users/tdelabro/Library/Application Support/cli-wallet.sqlite3")?;
    let manager = SqliteConnectionManager::file(&db_path);
    // let manager = SqliteConnectionManager::memory();
    tracing::info!("Connected to db at '{}'", db_path.to_str().unwrap());
    let pool = r2d2::Pool::new(manager)?;

    let mut db_conn = pool.get()?;
    wallet::db::create_tables(&mut db_conn)?;
    tracing::info!("Database initialized");

    let server = server::GenericService::new(server::MemoryDataService::new(pool))
        .serve(stdio())
        .await
        .inspect_err(|e| {
            tracing::error!("serving error: {:?}", e);
        })?;

    server.waiting().await?;

    Ok(())
}
