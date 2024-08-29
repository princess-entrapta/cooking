use core::fmt::Display;

use serde::{Deserialize, Serialize};

#[derive(Debug)]
pub struct AppError {
    pub reason: String,
}

impl Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(self.reason.as_str())
    }
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub enum Lang {
    #[serde(rename = "en")]
    En,
    #[serde(rename = "fr")]
    Fr,
}

impl Display for Lang {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::En => f.write_str("en"),
            Self::Fr => f.write_str("fr"),
        }
    }
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct Recipe {
    pub lang: Lang,
    pub title: String,
    pub slug: String,
    pub cooking_time_min: u32,
    pub preparation_time_min: u32,
    pub servings: u32,
    pub photo_url: String,
    pub preparation_steps: String,
    pub ingredients: Vec<Ingredient>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct Ingredient {
    pub lang: Lang,
    pub name: String,
    pub unit: String,
    pub amount: String,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct RecipeStore {
    pub title: Trad,
    pub slug: String,
    pub cooking_time_min: i64,
    pub preparation_time_min: i64,
    pub servings: u32,
    pub photo_url: String,
    pub preparation_steps: Trad,
    pub ingredients: Vec<IngredientStore>,
}
impl RecipeStore {
    pub fn search_tags(&self) -> Vec<String> {
        self.title
            .en
            .split(" ")
            .map(|s| s.to_lowercase())
            .chain(self.title.fr.split(" ").map(|s| s.to_lowercase()))
            .chain(
                <Vec<IngredientStore> as Clone>::clone(&self.ingredients)
                    .into_iter()
                    .map(|i| i.search_tags())
                    .flatten(),
            )
            .collect()
    }
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct IngredientStore {
    pub name: Trad,
    pub amount: f64,
    pub unit: String,
}

impl IngredientStore {
    pub fn search_tags(&self) -> Vec<String> {
        vec![self.name.en.to_lowercase(), self.name.fr.to_lowercase()]
    }
}
#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct Trad {
    pub en: String,
    pub fr: String,
}

impl Trad {
    pub fn translate(&self, lang: Lang) -> String {
        match lang {
            Lang::En => self.en.to_owned(),
            Lang::Fr => self.fr.to_owned(),
        }
    }
}
