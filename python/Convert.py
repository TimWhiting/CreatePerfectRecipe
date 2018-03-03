from Ingredient import *
import re 
from RecipeDatabase import *

class Unit:
    def __init__(self,name="",conversion = 1):
        self.name = name
        self.conversion = conversion
        
validIngredients = list()
validIngredients.append(IngredientValue(["powdered sugar","confectioner"],True,False,128))
validIngredients.append(IngredientValue(["flour"],True,False,128))
validIngredients.append(IngredientValue(["sugar"],True,False,201))
validIngredients.append(IngredientValue(["salt"],True,False,284.14247))
validIngredients.append(IngredientValue(["butter"],True,False,227))

validUnits = list()
validUnits.append(Unit("c",1))
validUnits.append(Unit("T",1/16))
validUnits.append(Unit("t",1/48))

def convertAmount(value,ingredient,unit):
    for validUnit in validUnits:
        if unit in validUnit.name:
            return value*ingredient.gramsPcup*validUnit.conversion
  
def findName(string):
    ingredientString = string.lower()
    for ingredient in validIngredients:
        for name in ingredient.name:
            if name in ingredientString:
                return ingredient
    
def getIngredientFromString(string):
    ing = Ingredient()
    ingredient = findName(string)
    ing.name = ingredient.name
    ing.amount = findAmount(string,ingredient)
    return ing  

def findAmount(string,ingredient):
    pattern = "(\d)*[ ]*(\d)*[/]?(\d)*[ ]*([ctT]).*"
    prog = re.compile(pattern)
    result = prog.match(string)
    if result is not None:
        groups = result.groups()
        print(groups)
        if groups[1] is None:
            if groups[2] is None:
                value = int(groups[0])
            value = int(groups[0])/int(groups[2])
        else:
            value = int(groups[0])+int(groups[1])/int(groups[2])
    else:
        print("Ingredient doesn't match {}".format(string))
    value = convertAmount(value,ingredient,groups[3].lower())
    print(value)
    print(ingredient.name)
    return value

def ConvertAllRecipes():
    raw = RawDatabase()
    recipes = raw.getRecipes()
    for recipejson in recipes:
        reciperaw = RecipeRawFromJSON(recipejson)
        
        print(recipe.ingredients[0])