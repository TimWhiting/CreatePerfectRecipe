import tensorflow as tf
import numpy as np
from Recipe import *
import csv
from Convert import *
from RecipeDatabase import *


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

    def train(self):
        if self.invert:
            print("Learning Inverted")
            size = self.input_size
            self.input_size = self.output_size
            self.output_size = size
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

        # Run forward step
        z0 = tf.add(tf.matmul(self.input, self.w_in), layers[0])
        for i in range(self.layers):
            forward = sigma(z0)
            if i != self.layers - 1:
                z0 = tf.add(tf.matmul(layers[i], self.weights[i]), layers[i + 1])
        self.z_out = tf.add(tf.matmul(forward, self.w_out), layer_out)
        self.forward_out = sigma(self.z_out)

        # Back propagate
        self.diff = tf.subtract(self.forward_out, self.output)
        cost = tf.multiply(self.diff, self.diff)
        self.step = tf.train.GradientDescentOptimizer(self.learningrate).minimize(cost)

        self.loss = tf.losses.mean_squared_error(self.output, self.forward_out)

        self.sess = tf.InteractiveSession()
        self.sess.run(tf.global_variables_initializer())

        self.recipes = RecipeDatabase()
        last_loss = 1
        diff = 1
        i = 0
        numNoChange = 0
        # for i in range(10):
        continueRunning = True
        while continueRunning:
            current_sum = 0
            count = 0
            batch_size = 1
            batch_count = 0
            feature_batch = []
            label_batch = []
            for recipe in self.recipes.getRecipes():
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
        denormalized = self.sess.run(self.diff,feed_dict=feed_dict)
        print(denormalized)
        #denormalized = self.forward_out.eval(feed_dict, self.sess)[0]
        #denormalized = self.recipes.deNormalizeRow(self.forward_out.eval(feed_dict, self.sess)[0])
        j = 0
        with open(recipename,'w') as writefile:
            for i in range(len(validIngredients)):
                if validIngredients[i].used:
                    writefile.write("{} {}\n".format(validIngredients[i].name[0],
                                            getAmount(validIngredients[i],2000 * denormalized[0][j])))
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


def main():
    # layers = input("How many layers?")
    # nodes = input("How many nodes per layer?")
    # recipeLearner = RecipeLearner((int)layers, (int)nodes)
    # (error, numepochs) = recipeLearner.train()
    getRandomRecipe()
    # runCSVDataCollection()
    # runCSVDataInvertedCollection()


if __name__ == '__main__':
    main()
