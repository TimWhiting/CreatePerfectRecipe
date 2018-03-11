import json
from bson.json_util import loads,dumps
from RecipeRaw import *
from Recipe import Recipe
from Ingredient import *

def decode_object(o):
    if '__RecipeRaw__' in o:
        r = RecipeRaw()
        recipe = o['__RecipeRaw__']
        r.web_scraper_order = recipe['web_scraper_order']
        r.web_scraper_start_url = recipe['web_scraper_start_url']
        r.cookies = recipe['cookies']
        r.cookies_href = recipe['cookies_href']
        r.category = recipe['category']
        r.recipe_link = recipe['recipe_link']
        r.recipe_link_href = recipe['recipe_link_href']
        r.ingredients = list()
        for ing in recipe['ingredients']:
            r.ingredients.append(decode_object(ing))
        r.prep_time = recipe['prep_time']
        r.cook_time = recipe['cook_time']
        r.total_time = recipe['total_time']
        r.instructions = list()
        for inst in recipe['instructions']:
            r.instructions = decode_object(inst)
        r.nutrition_facts = recipe['nutrition_facts']
        r.name = recipe['name']
        r.num_reviews = recipe['num_reviews']
        r.category_name = recipe['category_name']
        r.stars = recipe['stars']   
        return r
    elif '__Recipe__' in o:
        r = Recipe()
        recipe = o['__Recipe__']
        r.name = recipe['name']
        r.ratings = recipe['ratings']
        r.ingredients = list()
        for ing in recipe['ingredients']:
            r.ingredients.append(decode_object(ing))
        return r
    elif '__Ingredient__' in o:
        i = Ingredient()
        ing = o['__Ingredient__']
        i.name = ing['name']
        i.amount = ing['amount']
        return i
    elif 'ingredients' in o:
        return o['ingredients']
    elif 'instructions' in o:
        return o['instructions']
    else:
        print(o)
        return o

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        return {'__{}__'.format(o.__class__.__name__): o.__dict__}