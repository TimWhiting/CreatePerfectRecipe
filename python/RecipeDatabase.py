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
        self.columnMultipliers = []
        self.normalizedRows = [recipe.getInputVectorNormalized() for recipe in self.getRecipes()]
        self.fullyNormalizedRecipes = []
        if len(self.normalizedRows) > 0:
            self.computeColumnMultipliers()
    
    def cols(self, columnNumber):
        return [recipe[columnNumber] for recipe in self.normalizedRows]        
    
    def computeColumnMultipliers(self):
        for i in range(0, len(self.normalizedRows[0])):
            min0 = min(self.cols(i))
            max0 = max(self.cols(i))
            self.columnMultipliers.append([(min0), (max0 - min0)])
    
    def normalizeColumns(self):
        for i in range(0, len(self.normalizedRows)):
            temp = []
            for j in range(0, len(self.normalizedRows[0])):
                try:
                    temp.append((self.normalizedRows[i][j] - self.columnMultipliers[j][0]) / (self.columnMultipliers[j][1]))
                except:
                    print(j)
            self.fullyNormalizedRecipes.append(temp)
    
    def getNormalizedInputs(self, inputs):
        temp = []
        for j in range(0, len(inputs)):
            temp.append((inputs[j] - self.columnMultipliers[j][0]) / (self.columnMultipliers[j][1]))
        return temp
            
    def deNormalizeRow(self, inputRow):
        denormalizedRow = []
        for i in range(0, len(inputRow)):
            denormalizedRow.append((inputRow * self.columnMultipliers[i][1]) + self.columnMultipliers[i][0])
        return denormalizedRow