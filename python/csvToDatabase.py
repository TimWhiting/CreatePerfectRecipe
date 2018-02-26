from pymongo import MongoClient
import csv
from bson.json_util import loads
import json

class RecipeRaw:
    def __init__(self,row):
        self.web_scraper_order = row[0]
        self.web_scraper_start_url = row[1]
        self.cookies = row[2]
        self.cookies_href = row[3]
        self.category = row[4]
        self.category_href = row[5]
        self.recipe_link = row[6]
        self.recipe_link_href = row[7]
        self.ingredients = json.loads(row[8])
        self.ingredients.pop()
        self.prep_time = row[9]
        self.cook_time = row[10]
        self.total_time = row[11]
        self.instructions = json.loads(row[12])
        self.nutrition_facts = row[13]
        self.name = row[14]
        self.num_reviews = int(row[15])
        self.category_name = row[16]
        stars5 = int(row[17])
        stars4 = int(row[18])
        stars3 = int(row[19])
        stars2 = int(row[20])
        stars1 = int(row[21])
        self.stars = list()
        self.stars.extend([stars1,stars2,stars3,stars4,stars5])
        
    def getJSON(self):
        return loads(json.dumps(self,default=lambda o: o.__dict__))

class csvToDatabase:
    def __init__(self, csvFile):
        self.csvFile = csvFile
        
    def clearDatabase(self):
        client = MongoClient("mongodb://Jennings:#cookies1234567890!@45.56.50.200:50682/admin?authMechanism=SCRAM-SHA-1");
        db = client.recipes
        collection = db.recipes_raw
        collection.delete_many({})
        
    def loadToDatabase(self):
        invalid_categories = ["Cookie Icing and Frosting" , "Cake Mix Cookies"]
        client = MongoClient("mongodb://Jennings:#cookies1234567890!@45.56.50.200:50682/admin?authMechanism=SCRAM-SHA-1");
        db = client.recipes
        collection = db.recipes_raw
        with open(self.csvFile) as csvfile:
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
                            collection.insert_one(r.getJSON())
                    except:
                        pass
                    