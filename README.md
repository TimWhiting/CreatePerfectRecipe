# CreatePerfectRecipe
- Our CS 478 Team Project consists of gathering/formatting data and running several machine learning algortihms on data from recipe sites.
## Objective
- Train machine learning algorithms to rate recipes based on:
  - Ingredients
  - Time
  - Nutritional Value
  - Etc
## Phases
1. We use the Chrome Extension [WebScraper](http://webscraper.io/documentation) to get the raw data from recipe sites such as [AllRecipes](http://allrecipes.com/). 
2. We will then run some algorithms on the data to format it into a common format that can be run through a machine learning algorithm.
3. Finally we will train several machine learning algorithms (from [tensorflow](https://www.tensorflow.org/get_started/)) on the data.
4. We will test the machine learning model on novel recipes from some other site and compare them to reviews and try some of the best/worst ones out.
5. We will compile the results and present them to the class.
## Tools
- We will be programming/scripting in Python 3.6 using [Anaconda](https://www.anaconda.com/download/)
- We will be using [Jupyter Lab and Jupyter Notebooks](http://jupyter.org/documentation) from Anaconda where it makes sense
- We will be using [MongoDB](https://docs.mongodb.com/) for storing the data
- We will be using [pymongo v 3.4](http://api.mongodb.com/python/3.4.0/) for interacting with MongoDB
- We will be using [tensorflow](https://www.tensorflow.org/get_started/) for machine learning

## Repo Organization
Organization will go as follows:
Each folder will have a README.md with an explanation of what is in the folder and any subfolders
- ipynb is the folder where all of our code will go (both jupyter notebooks and python scripts)
- data is the folder where all data goes (database and scrapers)
