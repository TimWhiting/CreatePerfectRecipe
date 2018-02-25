from Recipe import *
from Ingredient import *
import csv

class csvToDatabase:
    def __init__(self, csvFile):
        with open(csvFile) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                    print(','.join(row))