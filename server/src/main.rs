use std::{path::PathBuf, str::FromStr};

use anyhow::Result;
use r2d2_sqlite::SqliteConnectionManager;
use rmcp::{ServiceExt, transport::stdio};
use tracing_subscriber::EnvFilter;
use wallet::seed_phrase;

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize the tracing subscriber with file and stdout logging
    tracing_subscriber::fmt()
        .with_env_filter(EnvFilter::from_default_env().add_directive(tracing::Level::DEBUG.into()))
        .with_writer(std::io::stderr)
        .with_ansi(false)
        .init();

    tracing::info!("Starting MCP server");

    let db_path = PathBuf::from_str("/tmp/cashu-mcp-db.sqlite3")?;
    let manager = SqliteConnectionManager::file(&db_path);
    tracing::info!("Connected to db at '{}'", db_path.to_str().unwrap());
    let pool = r2d2::Pool::new(manager)?;

    let mut db_conn = pool.get()?;
    wallet::db::create_tables(&mut db_conn)?;
    let seed_phrase_manager = wallet::wallet::sqlite::SeedPhraseManager::new(pool.clone())?;
    if !wallet::wallet::exists(&db_conn)? {
        let seed_phrase = seed_phrase::create_random()?;
        wallet::wallet::init(seed_phrase_manager, &db_conn, &seed_phrase)?;
        tracing::info!("Seed phrase initialized");
    }
    tracing::info!("Database initialized");

    let server = server::GenericService::new(server::SqliteCashuWalletService::new(pool))
        .serve(stdio())
        .await
        .inspect_err(|e| {
            tracing::error!("serving error: {:?}", e);
        })?;

    server.waiting().await?;

    Ok(())
}
