from pymongo import MongoClient
import csv
from Ingredient import *
from bson.json_util import loads,dumps
from JSONHelper import *
from RecipeRaw import *
from Recipe import *

client = MongoClient("mongodb://Jennings:#cookies1234567890!@45.56.50.200:50682/admin?authMechanism=SCRAM-SHA-1");
db = client.recipes
invalid_categories = ["Cookie Icing and Frosting" , "Cake Mix Cookies"]


    
class Database:
    def getRecipes(self):
        recipes = self.collection.find({})
        newRecipes = list()
        for recipe in recipes:
            recipesNew = decode_object(recipe)
            newRecipes.append(recipesNew)
        return newRecipes
    
    def clearDatabase(self):
        self.collection.delete_many({})
    
    def addRecipe(self,recipe):
        self.collection.insert_one(loads(json.dumps(recipe, cls=CustomEncoder)))
    
    
class RawDatabase(Database):
    def __init__(self):
        self.collection = db.recipes_raw
        
    def loadToDatabase(self,CSVFile):
        with open(CSVFile) as csvfile:
            reader = csv.reader(csvfile)
            i = 0
            for row in reader:
                if i == 0:
                    i = 1
                    print(",".join(row)+"\n")
                else:
                    try:
                        r = RecipeRawFromCSV(row)
                        if (r.category not in invalid_categories):
                            self.collection.insert_one(loads(json.dumps(r, cls=CustomEncoder)))
                    except:
                        pass
    
class RecipeDatabase(Database):
    def __init__(self):
        self.collection = db.recipes