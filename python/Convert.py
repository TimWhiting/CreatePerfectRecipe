from Ingredient import *
import re 
from RecipeDatabase import *
from RecipeRaw import *
from Recipe import *
class Unit:
    def __init__(self,name="",conversion = 1):
        self.name = name
        self.conversion = conversion
        
validIngredients = list()
validIngredients.append(IngredientValue(["egg"],True,True,1))
validIngredients.append(IngredientValue(["oil"],True,True,218))
validIngredients.append(IngredientValue(["water"],True,True,236.59))
validIngredients.append(IngredientValue(["butter","margarine"],True,True,227))
validIngredients.append(IngredientValue(["milk"],True,True,242))
validIngredients.append(IngredientValue(["vanilla"],True,True,208))

validIngredients.append(IngredientValue(["chocolate"],True,False,175))
validIngredients.append(IngredientValue(["cocoa powder"],True,False,118))
validIngredients.append(IngredientValue(["spice"],True,False,100))
validIngredients.append(IngredientValue(["baking powder"],True,False,230))
validIngredients.append(IngredientValue(["baking soda"],True,False,230.4))
validIngredients.append(IngredientValue(["brown sugar"],True,False,217))
validIngredients.append(IngredientValue(["powdered sugar","confectioner"],True,False,128))
validIngredients.append(IngredientValue(["flour"],True,False,128))
validIngredients.append(IngredientValue(["sugar"],True,False,201))
validIngredients.append(IngredientValue(["salt"],True,False,284.14247))

validUnits = list()
validUnits.append(Unit("c",1))
validUnits.append(Unit("T",1/16))
validUnits.append(Unit("t",1/48))

def convertAmount(value,ingredient,unit = "c"):
    for validUnit in validUnits:
        if unit in validUnit.name:
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
                ingredientList.append(ing)
            else:
                badRecipe = True
        if badRecipe is False:
            recipeNew = Recipe(reciperaw.name,reciperaw.stars,ingredientList)
            newDatabase.addRecipe(recipeNew)