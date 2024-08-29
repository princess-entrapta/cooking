import re
import requests
import bs4
import json

base_url = "https://based.cooking/"


slugs = [
    "zurich-sytle-meat-saute/",
    "kombucha/",
    "galinha-caipira/",
    "grilled-mackerel-with-miso-soup-and-squash/",
    "coconut-flour-bread/",
    "risengroed/",
    "spiced-apple-pancakes/",
    "strawberry-compote/",
    "tajine/",
    "granola/",
    "zaatar/",
    "grostoli/",
    "exotic-ginger-cumin-chicken/",
    "hakka-style-meatballs/",
    "one-pot-chicken-tetrazzini/",
    "smoked-salmon-pasta-primavera/",
    "spicy-kung-pao-style-chicken/",
    "bean-salad/",
    "zaatar-chicken-bulgur-bowls/",
    "beef-and-broccoli/",
    "egyptian-lentils/",
    "fajitas/",
    "irish-potato-casserole/",
    "mexican-meat-loaf/",
    "smoked-salmon-quiche/",
    "tabouleh/",
    "tofu-and-cashew-chow-mein/",
    "cuca-italiana/",
    "teriyaki-beef/",
    "cheddar-crusted-chicken/",
    "colcannon-bake/",
    "easy-chicken-and-rice-casserole/",
    "fall-vegetable-and-chickpea-curry/",
    "ham-and-lentil-soup/",
    "newfoundland-cod-chowder/",
    "panang-style-beef-curry/",
    "perfect-potato-salad/",
    "turkish-red-lentil-soup/",
    "turkish-style-spiced-chicken/",
    "turmeric-flatbread/",
    "winter-risotto/",
    "autumn-soup/",
    "greek-salad/",
    "gypsy-soup/",
    "ratatouille/",
    "red-lentil-dahl/",
    "shrimp-and-chicken-jambalaya/",
    "spinach-rice-casserole/",
    "chipolata-in-balsamic-vinegar/",
    "couscous/",
    "okroshka/",
    "seafood-pasta/",
    "scouse/",
    "korv-stroganoff/",
    "easy-pizza-sauce/",
    "wholemeal-pizza/",
    "dulce-de-leche/",
    "pulpo-gallega/",
    "wholemeal-wheat-flour-pizza-dough/",
    "banana-oatmeal-cookies/",
    "apple-chicken/",
    "ardei-umpluti/",
    "farci-tomatoes/",
    "chicken-satay/",
    "tarta-de-santiago/",
    "kettlecorn/",
    "fennel-beans-and-kale-soup/",
    "butter-based-biscuit/",
    "kettle-chips/",
    "shrimp-fettuccine-alfredo/",
    "tahini-short-bread/",
    "grands-peres/",
    "croque-monsieur/",
    "puff-pastry/",
    "torta-frita-criolla/",
    "pasta-arrabbiata/",
    "chicken-paprikash/",
    "pastitsio/",
    "peat-carrot-salad/",
    "dou-sha-bao/",
    "spicy-sausage-pasta/",
    "steak-tartare/",
    "potato-soup/",
    "lavacake/",
    "quiche/",
    "ceviche/",
    "cheese/",
    "chicken-tikka-masala/",
    "cream-cheese/",
    "frijol-con-puerco/",
    "greek-yogurt/",
    "honey-sriracha-chicken-thighs/",
    "ricotta/",
    "salsa/",
    "sardine-cakes/",
    "slow-cooked-lamb-with-lemon/",
    "tzatziki/",
    "baby-back-ribs/",
    "beef-wellington/",
    "full-english-breakfast/",
    "medieval-beef-soup/",
    "aussie-snags/",
    "beef-kidney/",
    "apple-pie/",
    "chocolate-chip-cookies/",
    "italian-mulled-wine/",
    "limoncello/",
    "mapo-tofu/",
    "mushroom-stragonov/",
    "ragu-napoletano/",
    "ravioli/",
    "soleier/",
    "chicken-tenders-airfried/",
    "chorizo-and-chickpea-soup/",
    "coleslaw/",
    "curry-sauce/",
    "honey-garlic-chicken/",
    "diannes-southwest-salad/",
    "tanzania-tea-with-milk/",
    "yorkshire-puddings/",
    "baked-pasta-with-broccoli/",
    "challah-bread/",
    "oatmeal-pancakes/",
    "quarkbaellchen/",
    "yibin-burning-noodles/",
    "burger-dressing/",
    "italian-bread/",
    "lenten-lentil-curry/",
    "mayonnaise-or-aioli/",
    "mazurek/",
    "okonomiyaki/",
    "orange-jam/",
    "ukrainian-vareniki/",
    "coriander-chicken/",
    "garam-masala/",
    "hoisin-pork-belly/",
    "ukrainian-borscht/",
    "lebanese-lentil-soup/",
    "shepherds-pie/",
    "turkey-smoked/",
    "spicy-mayo/",
    "torrijas/",
    "collard-greens-with-smoked-duck-and-parnips/",
    "demi-glace/",
    "hearty-breakfast-oatmeal/",
    "shakshouka/",
    "basic-meatballs/",
    "fondue/",
    "ricotta-lasagna-filling/",
    "spaghetti-all-amatriciana/",
    "turkish-yogurt-soup/",
    "asian-style-chicken-sticky-sauce/",
    "bolo-do-caco/",
    "bolognese-sauce/",
    "brown-sauce/",
    "corn-salsa/",
    "country-crisp-cereals/",
    "eggroll-in-a-bowl/",
    "erwtensoep/",
    "french-onion-soup/",
    "garlic-toast/",
    "lemon-and-oregano-chicken-traybake/",
    "lobster-bisque/",
    "meatloaf/",
    "miso-soup/",
    "paneer-tikka-masala/",
    "pepper-sauce/",
    "pho-soup/",
    "sourdough-potato-bread/",
    "simple-pasta-cream-sauce/",
    "sourdough-bread-with-seeds-and-grains/",
    "sourdough-starter/",
    "southern-biscuits/",
    "tofu-stir-fry/",
    "tuhu/",
    "apple-strudel/",
    "crab-salad/",
    "pasta-alla-norma/",
    "pate-chinois/",
    "sausage-rolls/",
    "zarangollo/",
    "assam-tea/",
    "babas-feta-pasta/",
    "baked-mostaccioli/",
    "belgian-pear-syrup/",
    "breakfast-wrap/",
    "cheesy-pasta-bake/",
    "cheesy-potatoe-bake/",
    "classic-bechamel-sauce/",
    "francesinha/",
    "french-toast/",
    "greek-easter-cookies/",
    "kalderetang-manok/",
    "kvass/",
    "lamb-biriyani/",
    "lasagna/",
    "loaded-mexican-rice/",
    "mushroom-risotto/",
    "nashville-chicken/",
    "no-knead-bread/",
    "no-knead-pizza-dough/",
    "onion-raitha/",
    "pan-pizza/",
    "pizza-sauce/",
    "savory-squash/",
    "schinkenfleckerl-gratinated/",
    "simple-chicken-curry/",
    "pork-carnitas/",
    "lentejas/",
    "sourdough-loaf/",
    "aglio-e-olio/",
    "spaghetti-alla-puttanesca/",
    "spanish-tortilla/",
    "stoemp/",
    "stoofvlees/",
    "swedish-pancakes/",
    "chicharrones/",
    "bloody-mary-mix/",
    "chimichanga/",
    "cinque-pi/",
    "gluehwein/",
    "hamburger-patties-all-beef/",
    "irish-coffee/",
    "orange-glorious/",
    "pozharskiye-cutlets/",
    "russian-1000-islands-sauce/",
    "salsa-verde/",
    "danish-pancake/",
    "lenten-chili/",
    "potato-leek-soup/",
    "schnitzel/",
    "shrimp-and-grits/",
    "baked-salmon/",
    "cannellini-bean-salad/",
    "cooked-chickpeas/",
    "dominican-spaghetti/",
    "fajita-seasoning/",
    "pilaf/",
    "aljotta/",
    "arroz-chaufa/",
    "bolinhos-de-coco/",
    "brigadeiro/",
    "chicken-in-red-wine-vinegar-sauce/",
    "chicken-soup/",
    "coconut-oil-coffee/",
    "lemon-juice-salad-dressing/",
    "party-mimosa/",
    "pickled-onions/",
    "red-sauce/",
    "stir-fried-chicken-with-an-orange-sauce/",
    "ginger-garlic-broccoli/",
    "butter-chicken-masala/",
    "fish-curry/",
    "frittata/",
    "naan-bread/",
    "gumbo-shrimp-and-sausage/",
    "tuna-salad/",
    "spatchcock-chicken/",
    "tomato-and-grilled-paprika-soup/",
    "zopf/",
    "breton-crepes/",
    "french-crepes/",
    "tomato-flavored-hamburger-macaroni/",
    "banana-pancakes/",
    "ginataang-kalabasa/",
    "hamburger-patties/",
    "hellfire-steak/",
    "hummus/",
    "oaty-pancakes/",
    "peanut-butter/",
    "quickbreakfastspaghetti/",
    "simple-sauce/",
    "spaghetti-and-meatballs/",
    "stuffed-round-squash/",
    "banana-muffins-with-chocolate/",
    "sweet-potato-fries/",
    "beef-goulash/",
    "cheesy-meatballs/",
    "chicken-pasta-casserole/",
    "pork-based-chili-con-carne/",
    "country-skillet/",
    "creamy-mashed-potatoes/",
    "guacamole/",
    "fried-anglerfish-fillet/",
    "fried-potatoes/",
    "hangover-eggs/",
    "japanese-noodle-soup/",
    "ketchup/",
    "maque-choux/",
    "merchants-buckwheat/",
    "omelet/",
    "pan-seared-chicken/",
    "parmesan-potatoes/",
    "pasta-navy-style/",
    "quesadilla/",
    "refried-beans/",
    "roasted-chicken-breast/",
    "roesti/",
    "scandinavian-coffee-cake/",
    "sticky-porkchops/",
    "sunday-milkshake/",
    "taco-meat/",
    "tortellini/",
    "tuna-sub/",
    "yogurt/",
    "banana-bread/",
    "beef-jerky/",
    "beef-tips/",
    "cacio-e-pepe/",
    "caesar-salad/",
    "carbonara/",
    "chicken-biscuit-potpie/",
    "chili-con-carne/",
    "croutons/",
    "dried-tomato-plum-spread/",
    "drunken-beans/",
    "flammkuchen/",
    "instant-tom-yam-kung-noodle-soup/",
    "liverpate/",
    "marinated-pork-steaks/",
    "matcha-cookies/",
    "miso-ginger-pork/",
    "pancake/",
    "pizza-dough/",
    "potato-and-eggplant-curry/",
    "ragu/",
    "sauerkraut/",
    "aelplermagronen/",
    "almeirim-stone-soup/",
    "stroganoff/",
    "portuguese-steak-with-beer-sauce/",
    "bread/",
    "broiled-trevally/",
    "carbonade/",
    "chicken-parmesan/",
    "chicken-stock-bone-broth/",
    "chicken-wings/",
    "chicken-tomato-spinach-curry/",
    "eggs/",
    "french-mustard-sauce-porkchops/",
    "gnocchi/",
    "oats/",
    "pasta/",
    "pasta-sauce/",
    "rice/",
    "chicken-tacos/",
    "beef-stew/",
    "tuscan-style-pork-roast/",
    "tiroler-groestl/",
]

final_json = []

for slug in slugs:
    print(slug)
    resp = requests.get(base_url + slug).text
    soup = bs4.BeautifulSoup(resp, features="html5lib")

    try:
        general, ingredients = soup.find_all("ul")[:2]
    except ValueError:
        ingredients = soup.find_all("ul")[0]
    try:
        prepare_time, cooking_time, servings = [
            int(re.search(r"[0-9]+", li.text).group(0)) for li in general.find_all("li")
        ]
    except AttributeError:
        prepare_time, cooking_time, servings = 0, 0, 0
        ingredients = general
    except ValueError:
        try:
            prepare_time, servings = [int(re.search(r"[0-9]+", li.text).group(0)) for li in general.find_all("li")]
            cooking_time = 0
        except ValueError:
            prepare_time = [int(re.search(r"[0-9]+", li.text).group(0)) for li in general.find_all("li")][0]
            servings = 0
            cooking_time = 0
    title = soup.find("h1").text.strip()
    try:
        steps = "\n".join([f"{i+1}. {li.text}" for i, li in enumerate(soup.find("ol").find_all("li"))])
    except AttributeError:
        steps = ""
    ingredients_raw = [i.text for i in ingredients.find_all("li")]
    ingredients = [
        {
            "unit": (
                re.search(
                    r"(cup|lb|tbsp|cups|tsp|teaspoon|tablespoon|oz|g|kg|l|mL)(s)?(\s|$)", i, flags=re.IGNORECASE
                ).group(1)
                if re.search(
                    r"(cup|lb|tbsp|cups|tsp|teaspoon|tablespoon|oz|g|kg|l|mL)(s)?(\s|$)", i, flags=re.IGNORECASE
                )
                else ""
            ),
            "amount": (
                eval(re.search(r"[0-9]+( ?/ ?[0-9]+)?(\.[0-9]+)?", i).group(0))
                if re.search(r"[0-9]+( ?/ ?[0-9]+)?(\.[0-9]+)?", i)
                else 0
            ),
            "name": {
                "en": re.sub(
                    r"[0-9/.]+\s?(cup|lb|tbsp|cups|tsp|teaspoon|tablespoon|oz|g|l|mL)(s)?(\s|$)",
                    "",
                    i,
                    1,
                    flags=re.IGNORECASE,
                ).strip(),
                "fr": "",
            },
        }
        for i in ingredients_raw
    ]

    img_url = soup.find("img")
    if not img_url or not img_url.attrs["src"].endswith(".webp"):
        img_url = ""
    else:
        img_url = img_url.attrs["src"]
    final_json.append(
        {
            "title": {"en": title, "fr": ""},
            "slug": slug[:-1],
            "cooking_time_min": cooking_time,
            "preparation_time_min": prepare_time,
            "servings": servings,
            "photo_url": f"/img/{slug[:-1]}.webp" if img_url else "",
            "preparation_steps": {"en": steps, "fr": ""},
            "ingredients": ingredients,
        }
    )

with open("data/recipe2.json", "w") as f:
    f.write(json.dumps(final_json))
