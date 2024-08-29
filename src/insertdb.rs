use redis::AsyncCommands;

use crate::indexing::InsertHandle;
use crate::schemas::{AppError, RecipeStore};
use futures::future::try_join_all;

impl From<redis::RedisError> for AppError {
    fn from(value: redis::RedisError) -> Self {
        return Self {
            reason: value.to_string(),
        };
    }
}

#[derive(Debug, Clone)]
pub struct RepositoryDb {
    client: redis::aio::MultiplexedConnection,
}

impl RepositoryDb {
    pub async fn new(redka_host: &str) -> Self {
        Self {
            client: redis::Client::open(format!("redis://{redka_host}").as_str())
                .unwrap()
                .get_multiplexed_tokio_connection()
                .await
                .unwrap(),
        }
    }
}

impl InsertHandle<String, String, RecipeStore, AppError> for RepositoryDb {
    async fn insert_tags(&self, tags: Vec<String>, item_ref: String) -> Result<(), AppError> {
        let item_ref_str = item_ref.as_str();
        try_join_all(tags.into_iter().map(|tag| async move {
            self.client
                .clone()
                .sadd::<String, String, Vec<String>>(
                    format!("tag.{}", tag.as_str()),
                    item_ref_str.to_owned(),
                )
                .await
        }))
        .await?;
        Ok(())
    }

    async fn insert_item(&self, item: RecipeStore) -> Result<(), AppError> {
        self.client
            .clone()
            .set::<&str, String, String>(
                format!("recipe.{}", item.slug).as_str(),
                serde_json::to_string(&item).unwrap(),
            )
            .await?;
        Ok(())
    }

    async fn insert_alias(&self, phrase: String, tags: Vec<String>) -> Result<(), AppError> {
        self.client
            .clone()
            .sadd::<_, _, Vec<String>>(format!("aliases.{phrase}"), tags)
            .await?;
        Ok(())
    }
}
