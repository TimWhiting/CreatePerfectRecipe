from Ingredient import *
from ValidIngredients import *
   
class Recipe:
    def __init__(self,name="",ratings=None,ingredients=list()):
        self.name = name
        if ratings is None:
            self.ratings = [0 for i in range(5)]
        else:
            self.ratings = ratings
        self.ingredients = ingredients
        
    def addRating(self,index,numReviews):
        self.ratings[index-1] = numReviews
        
    def getRating(self,index): 
        return self.ratings[index-1]
    
    def addIngredient(self,name,amount):
        ingredient = Ingredient(name,amount)
        self.ingredients.append(ingredient)
        
    def getInputVector(self):
        vector = List()
        for ing in validIngredients:
            for ingred in self.ingredients:
                if ingred.name in ing.name:
                    vector.append(ingred.amount)
                else:
                    vector.append(0)
        return vector
    def getOutputVector(self):
        return ratings
def getInputVectorSize():
    return len(validIngredients)
        
    