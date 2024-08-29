mod indexing;
mod insertdb;
mod schemas;
mod search;

use std::fs::File;

use futures::future::try_join_all;
use indexing::{insert_and_index_item, InsertHandle};
use insertdb::RepositoryDb;
use schemas::{AppError, RecipeStore};

async fn add_based_cooking_recipes(
    client: impl InsertHandle<String, String, RecipeStore, AppError>,
) {
    let recipes = File::open("data/recipe2.json").unwrap();
    let _ = try_join_all(
        serde_json::from_reader::<File, Vec<RecipeStore>>(recipes)
            .unwrap()
            .into_iter()
            .map(|recipe| {
                insert_and_index_item(
                    &client,
                    recipe.slug.clone(),
                    recipe.clone(),
                    recipe.search_tags(),
                )
            }),
    )
    .await;
}

pub async fn add_aliases(client: RepositoryDb) {
    let _ = client
        .insert_alias("cookie".to_string(), vec!["cookies".to_string()])
        .await;
    let _ = client
        .insert_alias("pancake".to_string(), vec!["pancakes".to_string()])
        .await;
    let _ = client
        .insert_alias("cookiez".to_string(), vec!["cookies".to_string()])
        .await;
    let _ = client
        .insert_alias(
            "sugar".to_string(),
            vec![
                "sugar".to_string(),
                "white sugar".to_string(),
                "brown_sugar".to_string(),
            ],
        )
        .await;
    let _ = client
        .insert_alias(
            "sucre".to_string(),
            vec![
                "sucre blanc".to_string(),
                "sucre".to_string(),
                "sucre brun".to_string(),
            ],
        )
        .await;
    let _ = client
        .insert_alias(
            "garlic".to_string(),
            vec!["garlic".to_string(), "garlic clove".to_string()],
        )
        .await;
    let _ = client
        .insert_alias("ail".to_string(), vec!["garlic".to_string()])
        .await;
    let _ = client
        .insert_alias("lemon".to_string(), vec!["lemon juice".to_string()])
        .await;
    let _ = client
        .insert_alias("citron".to_string(), vec!["jus de citron".to_string()])
        .await;
    let _ = client
        .insert_alias("sucre roux".to_string(), vec!["sucre brun".to_string()])
        .await;
}

#[tokio::main]

async fn main() {
    let client = RepositoryDb::new("localhost").await;
    //add_aliases(client)
    let _ = add_based_cooking_recipes(client).await;
}
