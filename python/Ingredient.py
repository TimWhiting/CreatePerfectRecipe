from bson.json_util import loads
import json

class IngredientValue:
    def __init__(self,name="",amount="1"):
        self.name = name
        self.amount = amount

class Ingredient:
    def __init__(self,name="",amount="1"):
        self.name = name
        self.amount = amount
        
    def getJSON(self):
        return loads(json.dumps(self,default=lambda o: o.__dict__))