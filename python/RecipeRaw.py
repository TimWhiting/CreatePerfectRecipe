from bson.json_util import loads,dumps
import json
from collections import namedtuple
import string
class RecipeRaw:
    def __init__(self,row = None):
        if row is not None:
            self.web_scraper_order = row[0]
            self.web_scraper_start_url = row[1]
            self.cookies = row[2]
            self.cookies_href = row[3]
            self.category = row[4]
            self.category_href = row[5]
            self.recipe_link = row[6]
            self.recipe_link_href = row[7]
            self.ingredients = json.loads(row[8])
            print(row[8])
            if "Add all ingredients" in self.ingredients[-1]:
                self.ingredients.pop()
            self.prep_time = row[9]
            self.cook_time = row[10]
            self.total_time = row[11]
            self.instructions = json.loads(row[12])
            self.nutrition_facts = row[13]
            self.name = row[14]
            self.num_reviews = int(row[15])
            self.category_name = row[16]
            try:
                self.stars = json.loads(row[17])
            except:
                stars5 = int(row[17])
                stars4 = int(row[18])
                stars3 = int(row[19])
                stars2 = int(row[20])
                stars1 = int(row[21])
                self.stars = list()
                self.stars.extend([stars1,stars2,stars3,stars4,stars5])
    
    def getJSON(self):
        return loads(json.dumps(self.__dict__))
    
def RecipeRawFromJSON(obj):
    row = list()
    row.extend([obj['web_scraper_order'],obj['web_scraper_start_url'],obj['cookies'],obj['cookies_href'],obj['category'],obj['category_href'],obj['recipe_link'],obj['recipe_link_href'],json.dumps(obj['ingredients']),obj['prep_time'],obj['cook_time'],obj['total_time'],json.dumps(obj['instructions']),obj['nutrition_facts'],obj['name'],str(obj['num_reviews']),obj['category_name'],json.dumps(obj['stars'])])
    return RecipeRaw(row)
      
       