import tensorflow as tf
import numpy as np
from Recipe import *
import csv
from Convert import *
from random import shuffle,randint
from RecipeDatabase import *
from sklearn.model_selection import train_test_split


def sigma(x):
    return tf.div(tf.constant(1.0), tf.add(tf.constant(1.0), tf.exp(tf.negative(x))))


def sigmaprime(x):
    return tf.multiply(sigma(x), tf.subtract(tf.constant(1.0), sigma(x)))


class RecipeLearner:
    input_size = getInputVectorSize()
    output_size = 5

    def __init__(self, l=1, n=30, learningrate=.1, invert=False, printBatch=False):
        self.invert = invert
        self.layers = l
        self.nodes = n
        self.printBatch = printBatch
        self.learningrate = learningrate
        self.recipes = RecipeDatabase()
        self.recipesList = self.recipes.getRecipes()
        if self.invert:
            print("Learning Inverted")
            size = self.input_size
            self.input_size = self.output_size
            self.output_size = size
            self.normalizedInputs = [self.recipes.getNormalizedOutputs(recipe.getOutputVector()) for recipe in self.recipesList]
            self.outputs = [recipe.getInputVectorNormalized() for recipe in self.recipesList]
        else:
            self.normalizedInputs = [self.recipes.getNormalizedInputs(recipe.getInputVectorNormalized()) for recipe in self.recipesList]
            self.outputs = [recipe.getOutputVector() for recipe in self.recipesList]
        self.trainI,self.testI,self.trainO,self.testO = train_test_split(np.array(self.normalizedInputs),np.array(self.outputs),test_size=.1,random_state=2)
        self.validIngredientNames = []
        for ing in validIngredients:
            if ing.used:
                self.validIngredientNames.append(ing.name[0].replace(" ","_"))
        self.trainIn = []
        self.testIn = []
        self.trainOut = []
        self.testOut = []
        stars = ["1","2","3","4","5"]
        self.trainIn = {'X':np.asarray(self.trainI)}
        self.trainOut = np.asarray(self.trainO)
        #self.trainOut.append({'X': tf.Variable(recipe.astype(np.float32))})
        #for recipe in self.trainI:
        #    self.trainIn.append(dict(zip(self.validIngredientNames,tf.Variable(recipe.astype(np.float32)))))
        #for ratings in self.trainO:
        #    self.trainOut.append(dict(zip(stars,tf.Variable(ratings.astype(np.float32)))))
        #for ratings in self.testO:
        #    self.testOut.append(dict(zip(stars,tf.Variable(ratings.astype(np.float32)))))
        #for recipe in self.testI:
        #    self.testIn.append(dict(zip(self.validIngredientNames, tf.Variable(recipe.astype(np.float32)))))
        #self.trainIn = np.array(self.trainIn)
        #self.trainOut = np.array(self.trainOut)
        #self.testIn = np.array(self.testIn)
        #self.testOut = np.array(self.testOut)


    def getInputBatch(self,batchSize = 1):
        return tf.estimator.inputs.numpy_input_fn(
            x=self.trainIn,
            y=self.trainOut,
            batch_size = batchSize,
            num_epochs=None,
            shuffle = True)
    def getRandomInput(self):
        return tf.estimator.inputs.numpy_input_fn(
            x ={'X':self.normalizedInputs[randint(0,len(self.recipesList)-1)].astype(np.float32)},
            batch_size = 1,
            num_epochs = None,
            shuffle = False)
    def getValidationInput(self,batchSize = 1):
        return tf.estimator.inputs.numpy_input_fn(
            x =self.trainIn,
            y=self.trainOut,
            batch_size = batchSize,
            num_epochs = None,
            shuffle = True)
    def _train(self):
        validation_metrics = {"MSE": tf.metrics.mean_squared_error}
        test_config = tf.estimator.RunConfig(save_checkpoints_secs=None,save_checkpoints_steps=1000)
        #features = [tf.feature_column.numeric_column(ing,shape=(1,)) for ing in self.validIngredientNames]
        features = [tf.feature_column.numeric_column("X",(self.input_size,))]
        regressor = tf.estimator.DNNRegressor(feature_columns=features,
                                               hidden_units=[self.nodes for i in range(self.layers)],
                                               label_dimension = self.output_size,
                                               optimizer = tf.train.GradientDescentOptimizer(.1),
                                               model_dir="training",
                                               config = test_config)
        numNoChange = 0
        diff = 1
        i = 0
        continueRunning = True
        lastmse = 0
        while continueRunning:
            regressor.train(input_fn=self.getInputBatch(batchSize=1))
            print("finished_training")
            eval_dict = regressor.evaluate(input_fn=self.getValidationInput(batchSize=1))
            mse = eval_dict['MSE']
            print("Epoch {}, {0.5f} MSE".format(i,eval_dict['MSE']))
           # y_pred = regressor.predict(self.getRandomInput())
            diff = abs(mse-lastmse)
            lastmse = mse
            print(mse)
            i += 1
            if diff < 0.001:
                numNoChange += 1
            if numNoChange > 10:
                continueRunning = False


    def train(self):
        #self._train()
        #return
        self.input = tf.placeholder(tf.float32, [None, self.input_size])
        self.output = tf.placeholder(tf.float32, [None, self.output_size])
        # Setup weights and layers
        self.w_in = tf.Variable(tf.truncated_normal([self.input_size, self.nodes]))
        layers = []
        self.weights = []
        for layer in range(self.layers):
            layers.append(tf.Variable(tf.truncated_normal([1, self.nodes])))
            if layer != self.layers - 1:
                self.weights.append(tf.Variable(tf.truncated_normal([self.nodes, self.nodes])))
        self.w_out = tf.Variable(tf.truncated_normal([self.nodes, self.output_size]))
        layer_out = tf.Variable(tf.truncated_normal([1, self.output_size]))
        z0 = []
        forward = []
        # Run forward step
        z0.append(tf.add(tf.matmul(self.input, self.w_in), layers[0]))
        for i in range(self.layers):
            forward.append(tf.nn.relu(z0[i]))
            if i != self.layers - 1:
                z0.append(tf.add(tf.matmul(layers[i], self.weights[i]), layers[i + 1]))
        self.z_out = tf.add(tf.matmul(forward[self.layers-1], self.w_out), layer_out)
        self.forward_out = tf.nn.relu(self.z_out)

        # Back propagate
        self.diff = tf.subtract(self.forward_out, self.output)
        cost = tf.multiply(self.diff, self.diff)
        self.step = tf.train.GradientDescentOptimizer(self.learningrate).minimize(cost)

        self.loss = tf.losses.mean_squared_error(self.output, self.forward_out)

        self.sess = tf.InteractiveSession()
        self.sess.run(tf.global_variables_initializer())


        last_loss = 1
        diff = 1
        i = 0
        numNoChange = 0
        # for i in range(10):
        continueRunning = True
        self.recipesList = self.recipes.getRecipes()
        while continueRunning:
            current_sum = 0
            count = 0
            batch_size = 1
            batch_count = 0
            feature_batch = []
            label_batch = []
            shuffle(self.recipesList)
            for recipe in self.recipesList:
                if batch_count >= batch_size:
                    feed_dict = {self.input: feature_batch, self.output: label_batch}
                    self.sess.run(self.step, feed_dict=feed_dict)
                    result = self.sess.run(self.loss, feed_dict=feed_dict)
                    current_sum += result
                    count += 1
                    if self.printBatch:
                        print("Batch", count * batch_size, " loss:", result)
                    batch_count = 0
                    feature_batch = []
                    label_batch = []
                else:
                    if not self.invert:
                        feature_batch.append(self.recipes.getNormalizedInputs(recipe.getInputVectorNormalized()))
                        label_batch.append(recipe.getOutputVector())
                    else:
                        feature_batch.append(self.recipes.getNormalizedOutputs(recipe.getOutputVector()))
                        label_batch.append(recipe.getInputVectorNormalized())
                    batch_count += 1
            if len(feature_batch) > 0:
                feed_dict = {self.input: feature_batch, self.output: label_batch}
                self.sess.run(self.step, feed_dict=feed_dict)
                result = self.sess.run(self.loss, feed_dict=feed_dict)
                current_sum += result
                count += 1
                if self.printBatch:
                    print("Batch", count * batch_size, " loss:", result)
            diff = abs(last_loss - current_sum / count)
            last_loss = current_sum / count
            i += 1
            print("Average accuracy for Epoch", i, ":", current_sum / count)
            if diff < 0.001:
                numNoChange += 1
            if numNoChange > 10:
                continueRunning = False
        return (current_sum / count, i)

    def saveWeights(self, filename):
        weights = []
        weights[1:self.layers + 1] = self.weights
        weights[0] = self.w_in
        weights[self.layers + 2] = self.w_out
        np.savetxt(filename, weights)

    def loadWeights(self, filename):
        weights = np.loadtxt(filename)
        self.w_in = weights[0]
        self.w_out = weights[self.layers + 2]
        self.weights = weights[1: self.layers + 1]

    def getOutput(self, inputs,recipename):
        labels = [0 for i in range(self.output_size)]
        feed_dict = {self.input: [inputs],self.output : [labels]}
        denormalized = self.diff.eval(feed_dict=feed_dict)
        print(denormalized)
        #denormalized = self.forward_out.eval(feed_dict, self.sess)[0]
        denormalized = self.recipes.deNormalizeRow(self.forward_out.eval(feed_dict, self.sess)[0])
        j = 0
        with open(recipename,'w') as writefile:
            for i in range(len(validIngredients)):
                if validIngredients[i].used:
                    writefile.write("{} {}\n".format(validIngredients[i].name[0],
                                            getAmount(validIngredients[i],2000 * denormalized[j])))
                    j += 1

    def getBestAndWorst(self):
        bestRating = 0
        worstRating = 100
        bestRecipe = None
        worstRecipe = None
        for recipe in self.recipes.getRecipes():
            labels = [0 for i in range(self.output_size)]
            feed_dict = {self.input:[self.recipes.getNormalizedInputs(recipe.getInputVectorNormalized())],self.output: [labels]}
            values = self.diff.eval(feed_dict=feed_dict)[0]
            #values = recipe.getOutputVector()
            print(values)
            rating = values[0]*1 + values[1]*2 + values[2]*3 + values[3]*4 + values[4]*5
            if rating > bestRating:
                bestRating = rating
                bestRecipe = recipe
            if rating < worstRating:
                worstRating = rating
                worstRecipe = recipe
        print(bestRating)
        print(worstRating)
        recipes = [bestRecipe, worstRecipe]
        names = ["bestrecipe.txt", "worstrecipe.txt"]
        # denormalized = self.forward_out.eval(feed_dict, self.sess)[0]
        #denormalized = self.recipes.deNormalizeRow(self.forward_out.eval(feed_dict, self.sess)[0])
        for i in range(len(recipes)):
            recipe = recipes[i]
            name = names[i]
            j = 0
            with open(name, 'w') as writefile:
                writefile.write("Recipe Name: {}\n".format(recipe.name))
                for i in range(len(validIngredients)):
                    if validIngredients[i].used:
                        if validIngredients[i].used:
                            writefile.write("{} {}\n".format(validIngredients[i].name[0],
                                                             getAmount(validIngredients[i],recipe.getInputVector()[j])))
                            j += 1

def runCSVDataCollection():
    with open('learning.csv', 'w') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',')
        csvWriter.writerow(['layers', 'nodes', 'MSE', 'Number of Epochs'])
        learningRates = [.05, .06, .07, .08, .09, .1, .125, .15, .175, .2, .25, .3, .35, .4]
        for i in range(1, 20):
            for j in range(1, 20):
                for k in learningRates:
                    recipeLearner = RecipeLearner(i, j, k, False, False)
                    (error, numepochs) = recipeLearner.train()
                    csvWriter.writerow([i, j, k, error, numepochs])


def runCSVDataInvertedCollection():
    with open('learning.csv', 'w') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',')
        csvWriter.writerow(['layers', 'nodes', 'MSE', 'Number of Epochs'])
        learningRates = [.05, .06, .07, .08, .09, .1, .125, .15, .175, .2, .25, .3, .35, .4]
        for i in range(1, 20):
            for j in range(1, 20):
                for k in learningRates:
                    recipeLearner = RecipeLearner(i, j, k, True, False)
                    (error, numepochs) = recipeLearner.train()
                    csvWriter.writerow([i, j, k, error, numepochs])


def getRandomRecipe():
    recipeLearner = RecipeLearner(2, 50, .1, True, False)
    recipeLearner.train()
    recipeLearner.getOutput([0, 0, 0, 0, 1],"good recipe.txt")
    recipeLearner.getOutput([1,1,1,0,0],"bad recipe.txt")

def getRecipes():
    recipeLearner = RecipeLearner(1, 50, .1, False, False)
    recipeLearner.train()
    recipeLearner.getBestAndWorst()


def main():
    # layers = input("How many layers?")
    # nodes = input("How many nodes per layer?")
    # recipeLearner = RecipeLearner((int)layers, (int)nodes)
    # (error, numepochs) = recipeLearner.train()
    getRandomRecipe()
    #getRecipes()
    # runCSVDataCollection()
    # runCSVDataInvertedCollection()


if __name__ == '__main__':
    main()
