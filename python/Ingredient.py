from bson.json_util import loads
import json


class IngredientValue:
    def __init__(self,name="",used = False, wet = False,gramsPcup=128,ingredient = None):
        if ingredient is None:
            self.name = name
            self.used = used
            self.wet = wet
            self.gramsPcup = gramsPcup
        else:
            self.name = ingredient.name
            self.used = False
            self.wet = False
            self.gramsPcup = 128


class Ingredient:
    def __init__(self,name="",amount="1"):
        self.name = name
        self.amount = amount

