from pymongo import MongoClient
import csv
from RecipeRaw import RecipeRaw

client = MongoClient("mongodb://Jennings:#cookies1234567890!@45.56.50.200:50682/admin?authMechanism=SCRAM-SHA-1");
db = client.recipes
invalid_categories = ["Cookie Icing and Frosting" , "Cake Mix Cookies"]

class Database:
    def getRecipes(self):
        return self.collection.find({})
    
    def clearDatabase(self):
        self.collection.deleteMany({})
    
    def addRecipe(self,recipe):
        self.collection.insert_one(recipe)
    
    
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
                        r = RecipeRaw(row)
                        if (r.category not in invalid_categories):
                            self.collection.insert_one(r.getJSON())
                    except:
                        pass
    
class RecipeDatabase(Database):
    
    def __init__(self):
        self.collection = db.recipes