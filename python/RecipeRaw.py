import json
from collections import namedtuple
import string
class RecipeRaw:
    def __init__(self,web=None,web_url=None,cookies=None,cookies_url=None,category=None,category_url=None,recipe=None,recipe_url=None,ingredients=None,prep_time=None,cook_time=None,total_time=None,instructions=None,nutrition=None,name=None,num_reviews=None,category_name=None,stars=None):
        self.web_scraper_order = web
        self.web_scraper_start_url = web_url
        self.cookies = cookies
        self.cookies_href = cookies_url
        self.category = category_url
        self.recipe_link = recipe
        self.recipe_link_href = recipe_url
        self.ingredients = ingredients
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.total_time = total_time
        self.instructions = instructions
        self.nutrition_facts = nutrition
        self.name = name
        self.num_reviews = num_reviews
        self.category_name = category_name
        self.stars = stars   
    
def RecipeRawFromCSV(row):
    ingredients = json.loads(row[8])
    ingredients.pop()
    instructions = json.loads(row[12])
    stars5 = int(row[17])
    stars4 = int(row[18])
    stars3 = int(row[19])
    stars2 = int(row[20])
    stars1 = int(row[21])
    stars = list()
    stars.extend([stars1,stars2,stars3,stars4,stars5])
    return RecipeRaw(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],ingredients,row[9],row[10],row[11],instructions,row[13],row[14],int(row[15]),row[16],stars)

def RecipeRawFromJSON(obj):
    ingredients = list()
    instructions = list()
    stars = list()
    #print(obj['stars'])
    for instruction in obj['instructions']:
        instructions.append(instruction['instructions'])
    for ingredient in obj['ingredients']:
        ingredients.append(ingredient['ingredients'])
    for star in obj['stars']:
        stars.append(star)
    return RecipeRaw(obj['web_scraper_order'],obj['web_scraper_start_url'],obj['cookies'],obj['cookies_href'],obj['category'],obj['category_href'],obj['recipe_link'],obj['recipe_link_href'],ingredients,obj['prep_time'],obj['cook_time'],obj['total_time'],instructions,obj['nutrition_facts'],obj['name'],str(obj['num_reviews']),obj['category_name'],stars)
      
       