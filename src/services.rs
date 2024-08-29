use std::usize;

use crate::schemas::{AppError, Ingredient, Lang, Recipe};
use crate::schemas::{IngredientStore, RecipeStore};
use crate::search::{ItemRepo, SearchDb};

use tokio::task::JoinError;

impl From<JoinError> for AppError {
    fn from(value: JoinError) -> Self {
        Self {
            reason: value.to_string(),
        }
    }
}

impl Ingredient {
    pub fn from_store(store_ingredient: IngredientStore, lang: Lang) -> Self {
        let mut amount = store_ingredient.amount.to_string();
        if store_ingredient.amount >= 10.0 {
            amount = store_ingredient.amount.to_string();
        }
        Self {
            lang: lang.clone(),
            name: store_ingredient.name.translate(lang),
            unit: store_ingredient.unit,
            amount: amount,
        }
    }
}

impl Recipe {
    pub fn from_store(recipe: RecipeStore, lang: &Lang) -> Self {
        Self {
            title: recipe.title.translate(lang.clone()),
            lang: lang.clone(),
            slug: recipe.slug.clone(),
            cooking_time_min: recipe.cooking_time_min as u32,
            preparation_time_min: recipe.preparation_time_min as u32,
            servings: recipe.servings,
            photo_url: recipe.photo_url,
            preparation_steps: recipe.preparation_steps.translate(lang.clone()),
            ingredients: recipe
                .ingredients
                .into_iter()
                .map(|i| Ingredient::from_store(i, lang.clone()))
                .collect(),
        }
    }
}

pub async fn find_recipes(
    db: impl ItemRepo<String, String, RecipeStore, AppError>,
    lang: Lang,
    search_query: &str,
    page_num: usize,
) -> Result<(Vec<Recipe>, usize), AppError> {
    let (recipes, nb_items) = db
        .get_items_for_search(search_query, 12, 3, 18, page_num)
        .await?;

    Ok((
        recipes
            .into_iter()
            .map(|r| Recipe::from_store(r, &lang))
            .collect(),
        nb_items,
    ))
}

pub async fn find_recipe(
    db: impl SearchDb<String, String, RecipeStore, AppError>,
    lang: Lang,
    slug: String,
) -> Result<Recipe, AppError> {
    Ok(Recipe::from_store(db.get_item_from_ref(slug).await?, &lang))
}
