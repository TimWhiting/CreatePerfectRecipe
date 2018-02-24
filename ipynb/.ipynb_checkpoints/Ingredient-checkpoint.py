import json
class Ingredient:
    def __init__(self,name="",amount="1"):
        self.name = name
        self.amount = amount
        
    def getJSON(self):
        return json.dumps(self,default=lambda o: o.__dict__,sort_keys=True,indent=4);