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
validIngredients.append(IngredientValue(["butter","margarine","shortening"],True,True,227))
validIngredients.append(IngredientValue(["cream cheese","whipping cream","whipped","cream","creme"],True,True,227))#not sure
validIngredients.append(IngredientValue(["milk"],True,True,242))
validIngredients.append(IngredientValue(["vanilla"],True,True,208))
validIngredients.append(IngredientValue(["vegetables","zucchini","pumpkin"],True,True,200))#not sure
validIngredients.append(IngredientValue(["extracts","lemon extract","mint extract","mint","lemon"],True,True,200))#not sure
validIngredients.append(IngredientValue(["food coloring"],True,True,208))
validIngredients.append(IngredientValue(["fruit","raisin","raspberry","date","orange","cherries","cranberries","strawberries","grape","cherry","preserves","jam","apple"],True,True,200))#not sure
#dry ingredients
validIngredients.append(IngredientValue(["nuts","almond","peanut","pecan","walnut","nut"],True,False,100))#not sure
validIngredients.append(IngredientValue(["mix"],False,False,0))
validIngredients.append(IngredientValue(["chocolate"],True,False,175))#not sure
validIngredients.append(IngredientValue(["cocoa powder"],True,False,118))#not sure
validIngredients.append(IngredientValue(["corn starch","cornstarch"],True,False,118))#not sure
validIngredients.append(IngredientValue(["spice", "nutmeg", "cinnamon","ginger","clove","cardamom"],True,False,100))#not sure
validIngredients.append(IngredientValue(["baking powder"],True,False,230))
validIngredients.append(IngredientValue(["baking soda"],True,False,230.4))
validIngredients.append(IngredientValue(["brown sugar"],True,False,217))
validIngredients.append(IngredientValue(["syrups","molasses","honey","corn syrup","maple syrup"],True,True,270)) #not sure
validIngredients.append(IngredientValue(["powdered sugar","confectioner"],True,False,128))
validIngredients.append(IngredientValue(["oat","granola"],True,False,100))#not sure
validIngredients.append(IngredientValue(["graham cracker","crisp rice","crispy rice"],True,False,100))#not sure
validIngredients.append(IngredientValue(["coconut"],True,False,100))#not sure
validIngredients.append(IngredientValue(["flour"],True,False,128))
validIngredients.append(IngredientValue(["sugar"],True,False,201))
validIngredients.append(IngredientValue(["salt"],True,False,284.14247))

validUnits = list()
validUnits.append(Unit(["cup","c"],1))
validUnits.append(Unit(["tablespoons"],1/16))
validUnits.append(Unit(["teaspoons"],1/48))
validUnits.append(Unit(["T"],1/16))
validUnits.append(Unit(["t"],1/16))

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