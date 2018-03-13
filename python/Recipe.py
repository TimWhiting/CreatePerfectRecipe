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
        vector = list()
        for ing in validIngredients:
            found = False
            for ingred in self.ingredients:
                if ingred.name in ing.name:
                    found = True
                    vector.append(ingred.amount)
            if not found:
                vector.append(0)
        return vector
    def getInputVectorNormalized(self):
        vector = list()
        totalWeight = 0
        for ingred in self.ingredients:
            totalWeight = totalWeight + ingred.amount
        for ing in validIngredients:
            found = False
            for ingred in self.ingredients:
                if ingred.name in ing.name:
                    found = True
                    vector.append(ingred.amount/totalWeight)
            if not found:
                vector.append(0)
        return vector
    def getOutputVector(self):
        totalRatings = 0
        newRatings = list()
        for rat in self.ratings:
            totalRatings = totalRatings + rat
        for rat in self.ratings:
            newRatings.append(rat/totalRatings)
        return newRatings
    
def getInputVectorSize():
    return len(validIngredients)
        
    