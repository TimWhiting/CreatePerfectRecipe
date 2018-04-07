from Ingredient import *
from Units import *
validIngredients = list()
validIngredients.append(IngredientValue(["egg"],True,True,60))
validIngredients.append(IngredientValue(["oil"],True,True,218))
validIngredients.append(IngredientValue(["water"],False,True,236.59))
validIngredients.append(IngredientValue(["butter","margarine","shortening", "lard"],True,True,227))
validIngredients.append(IngredientValue(["grains","oats","cornflakes", "granola", "flaxseed", "anise"],True,True,100))#approximately
validIngredients.append(IngredientValue(["candy", "lollipop", "marshmallows", "caramels", "licorice", "dulce de leche", "toffee"],True,True,200))#not sure on gms/cup for these
validIngredients.append(IngredientValue(["cream cheese","whipping cream","whipped","cream","creme"],True,True,227))#not sure
validIngredients.append(IngredientValue(["milk"],True,True,242))
validIngredients.append(IngredientValue(["vanilla"],True,True,208))
validIngredients.append(IngredientValue(["vegetables","zucchini","pumpkin"],True,True,200))#not sure
validIngredients.append(IngredientValue(["extracts","lemon extract","mint extract","mint","lemon"],True,True,200))#not sure
validIngredients.append(IngredientValue(["food coloring"],True,True,208))
validIngredients.append(IngredientValue(["fruit","raisin","raspberry","date","orange","cherries","cranberries","strawberries","grape","cherry","preserves","jam","apple", "blueberries", "apricot", "banana"],True,True,200))#not sure
#dry ingredients
validIngredients.append(IngredientValue(["nuts","almond","peanut","pecan","walnut","nut"],True,False,100))#not sure
validIngredients.append(IngredientValue(["mix"],False,False,100))
validIngredients.append(IngredientValue(["chocolate"],True,False,175))#not sure
validIngredients.append(IngredientValue(["cocoa powder"],True,False,118))#not sure
validIngredients.append(IngredientValue(["corn starch","cornstarch"],True,False,118))#not sure
validIngredients.append(IngredientValue(["spice", "nutmeg", "cinnamon","ginger","clove","cardamom", "pepper", "pepper", "rosemary", "poppy", "lavender"],True,False,100))#not sure
validIngredients.append(IngredientValue(["baking powder"],True,False,230))
validIngredients.append(IngredientValue(["baking soda"],True,False,230.4))
validIngredients.append(IngredientValue(["brown sugar"],True,False,217))
validIngredients.append(IngredientValue(["syrup","molasses","honey","corn syrup","maple syrup"],True,True,270)) #not sure
validIngredients.append(IngredientValue(["powdered sugar","confectioner"],True,False,128))
validIngredients.append(IngredientValue(["oat","granola"],True,False,100))#not sure
validIngredients.append(IngredientValue(["graham cracker","crisp rice","crispy rice"],True,False,100))#not sure
validIngredients.append(IngredientValue(["coconut"],False,False,100))#not sure
validIngredients.append(IngredientValue(["flour"],True,False,128))
validIngredients.append(IngredientValue(["sugar"],True,False,201))
validIngredients.append(IngredientValue(["salt"],True,False,284.14247))

validUnits = list()
validUnits.append(Unit(["cup","c"],1))
validUnits.append(Unit(["tablespoons"],1/16))
validUnits.append(Unit(["teaspoons"],1/48))
validUnits.append(Unit(["T"],1/16))
validUnits.append(Unit(["t"],1/16))
