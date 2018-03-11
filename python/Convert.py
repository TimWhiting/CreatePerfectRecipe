from Ingredient import *
import re 
from RecipeDatabase import *
from RecipeRaw import *
from Recipe import *
from ValidIngredients import *
from Units import *

     
def convertAmount(value,ingredient,unit = "c"):
    for validUnit in validUnits:
        for name in validUnit.name:
            if name in unit:
                return value*ingredient.gramsPcup*validUnit.conversion
  
def findName(string):
    ingredientString = string.lower()
    for ingredient in validIngredients:
        for name in ingredient.name:
            if name in ingredientString:
                return ingredient
    return None
    
def getIngredientFromString(string):
    ing = Ingredient()
    ingredient = findName(string)
    if ingredient is not None:
        ing.name = ingredient.name[0]
        ing.amount = findAmount(string,ingredient)
        return ing
    print("Ingredient doesn't match {}".format(string))

def findAmount(string,ingredient):
    value = None
    patternRegular = "(\d)*[ ]*(\d)*[/]?(\d)*[ ]*([ctT]).*"
    patternDirectAmount = "(\d)*[ ]*(\d)*[/]?(\d)*.*"
    patterns = [patternRegular, patternDirectAmount]
    for pattern in patterns:
        prog = re.compile(pattern)
        result = prog.match(string)
        if result is not None:
            groups = result.groups()
            if groups[1] is None:
                if groups[2] is None:
                    if groups[0] is None:
                        print("Ingredient amount doesn't match regex {}".format(string))
                        print(ingredient.name)
                        return 1
                    else:
                        value = int(groups[0])
                else:
                    value = int(groups[0])/int(groups[2])
            else:
                value = int(groups[0])+(int(groups[1])/int(groups[2]))
        else:
            continue
        if value is None:
            print("Ingredient amount doesn't match regex {}".format(string))
            print(value)
            print(ingredient.name)
            return 1
        if len(groups) is not 3:
            value = convertAmount(value,ingredient,groups[3].lower())
        else:
            value = convertAmount(value,ingredient)
        
        return value

def ConvertAllRecipes():
    raw = RawDatabase()
    newDatabase = RecipeDatabase()
    recipes = raw.getRecipes()
    badRecipe = False
    for reciperaw in recipes:
        badRecipe = False
        ingredientList = list()
        for ingredient in reciperaw.ingredients:
            #print(ingredient)
            ing = getIngredientFromString(ingredient)
            if ing is not None:
                if "mix" in ing.name:
                    badRecipe = True
                else:
                    Found = False
                    for ingred in ingredientList: #say if a recipe calls for butter and shortening
                        if ingred.name in ing.name:
                            ingred.amount = ingred.amount + ing.amount
                            Found = True
                    if not Found:
                        ingredientList.append(ing)
            else:
                badRecipe = False
        if badRecipe is False:
            recipeNew = Recipe(reciperaw.name,reciperaw.stars,ingredientList)
            newDatabase.addRecipe(recipeNew)