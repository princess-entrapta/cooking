use crate::pow::PowValidator;
use crate::schemas::Lang;
use crate::search::ItemRepo;
use crate::templates;
use crate::{services, Repositories};
use axum::extract::{Path, Query, State};
use axum::http::StatusCode;
use axum::response::IntoResponse;
use axum::{Form, Json};
use handlebars::Handlebars;
use serde::{Deserialize, Serialize};
use serde_json::json;
use spow::pow::Pow;
use std::collections::HashMap;

pub async fn search_recipe(
    State(repo): State<Repositories>,
    Query(search_params): Query<HashMap<String, String>>,
    Path(lang): Path<Lang>,
) -> impl IntoResponse {
    let reg = Handlebars::new();
    let search_page = search_params
        .get("page")
        .unwrap_or(&"1".to_owned())
        .parse::<usize>()
        .unwrap();
    let search_query = search_params
        .get("search")
        .unwrap_or(&"".to_owned())
        .to_string();
    let result =
        services::find_recipes(repo.db, lang.clone(), search_query.as_str(), search_page).await;
    if result.is_err() {
        tracing::error!("{:?}", result.unwrap_err());
        return StatusCode::INTERNAL_SERVER_ERROR.into_response();
    }
    let (recipes, count_total) = result.unwrap();
    let title_en = "Your results:";
    let title_fr = "Vos résultats :";
    let back_en = "Back";
    let back_fr = "Retour";
    let mut last_page = Some((count_total as f32 / 18.0).ceil() as usize);
    let mut next_page = Some(search_page + 1);
    if last_page <= Some(search_page) {
        last_page = None;
        next_page = None;
    }
    tracing::info!("Starting handlebars");
    axum::response::Html::from(
        reg.render_template(
            templates::SEARCH_RESULT_TEMPLATE,
            &json!({"recipe": recipes, 
            "search_query": search_query,
            "next_page": next_page,
            "prev_page": search_page - 1,
            "last_page": last_page,
            "trad_results": match lang.clone() {
                Lang::En => title_en,
                Lang::Fr => title_fr
            }, "trad_back": match lang { 
                Lang::En => back_en,
                Lang::Fr => back_fr
            },}),
        )
        .unwrap(),
    )
    .into_response()
}

pub async fn get_recipe(
    State(repo): State<Repositories>,
    Path((lang, slug)): Path<(Lang, String)>,
) -> impl IntoResponse {
    let reg = Handlebars::new();
    let result = services::find_recipe(repo.db.get_db(), lang.clone(), slug).await;
    if result.is_err() {
        tracing::error!("{:?}", result.unwrap_err().reason);
        return StatusCode::INTERNAL_SERVER_ERROR.into_response();
    }
    let mut recipe = result.unwrap();
    recipe.preparation_steps = markdown::to_html(&recipe.preparation_steps);
    let preparation_en = "Preparation time (min)";
    let preparation_fr = "Temps de préparation (min)";
    let cooking_en = "Cooking time (min)";
    let cooking_fr = "Temps de cuisson (min)";
    let servings_en = "Number of servings";
    let servings_fr = "Nombre de parts";
    axum::response::Html::from(
        reg.render_template(
            templates::RECIPE_TEMPLATE,
            &json!({"recipe": recipe,
            "trad_preparation": match lang {
                Lang::En => preparation_en,
                Lang::Fr => preparation_fr
            }, "trad_cooking": match lang {
                Lang::En => cooking_en,
                Lang::Fr => cooking_fr
            }, "trad_servings": match lang {
                Lang::En => servings_en,
                Lang::Fr => servings_fr
            }}),
        )
        .unwrap(),
    )
    .into_response()
}

pub async fn get_challenge_form() -> impl IntoResponse {
    let reg = Handlebars::new();

    // Create a new PoW which will be valid for 60 seconds
    let pows: Vec<_> = (0..16)
        .map(|_i| Pow::with_difficulty(18, 600).unwrap().to_string())
        .collect();

    // Create a puzzle challenge from this pow.
    // You can either call `build_challenge()` or `.to_string()`.
    axum::response::Html::from(
        reg.render_template(templates::CONTACT_FORM, &json!({"challenges": pows}))
            .unwrap(),
    )
    .into_response()
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct SubmitForm {
    body: String,
    challenges: [String; 16],
}

pub async fn post_form(
    State(repo): State<Repositories>,
    Json(submit): Json<SubmitForm>,
) -> impl IntoResponse {
    if !repo
        .db
        .get_pow_validator()
        .is_valid_pow(submit.challenges)
        .await
    {
        return StatusCode::BAD_REQUEST;
    }
    tracing::info!("{:?}", submit.body);
    StatusCode::OK
}
