import tensorflow as tf
import numpy as np
from Recipe import *
from RecipeDatabase import *

def sigma(x):
    return tf.div(tf.constant(1.0), tf.add(tf.constant(1.0), tf.exp(tf.negative(x))))

def sigmaprime(x):
    return tf.multiply(sigma(x), tf.subtract(tf.constant(1.0), sigma(x)))

class RecipeLearner:
    input_size = getInputVectorSize()
    output_size = 5

    def __init__(self, l=1, n=30):
        self.layers = l
        self.nodes = n

    def train(self):
        input = tf.placeholder(tf.float32, [None, self.input_size])
        output = tf.placeholder(tf.float32, [None, self.output_size])
        # Setup weights and layers
        w_in = tf.Variable(tf.truncated_normal([self.input_size, self.nodes]))
        layers = []
        weights = []
        for layer in range(self.layers):
            layers.append(tf.Variable(tf.truncated_normal([1, self.nodes])))
            if layer != self.layers - 1:
                weights.append(tf.Variable(tf.truncated_normal([self.nodes, self.nodes])))
        w_out = tf.Variable(tf.truncated_normal([self.nodes, self.output_size]))
        layer_out = tf.Variable(tf.truncated_normal([1, self.output_size]))

        # Run forward step
        z0 = tf.add(tf.matmul(input, w_in), layers[0])
        for i in range(self.layers):
            forward = sigma(z0)
            if i != self.layers - 1:
                z0 = tf.add(tf.matmul(layers[i], weights[i]), layers[i+1])
        z_out = tf.add(tf.matmul(forward, w_out), layer_out)
        forward_out = sigma(z_out)

        # Back propagate
        diff = tf.subtract(forward_out, output)
        cost = tf.multiply(diff, diff)
        step = tf.train.GradientDescentOptimizer(0.1).minimize(cost)

        loss = tf.losses.mean_squared_error(output, forward_out)

        sess = tf.InteractiveSession()
        sess.run(tf.global_variables_initializer())

        recipes = RecipeDatabase()
        last_loss = 1
        diff = 1
        i = 0
        # for i in range(10):
        while diff > 0.001:
            current_sum = 0
            count = 0
            batch_size = 1
            batch_count = 0
            feature_batch = []
            label_batch = []
            for recipe in recipes.getRecipes():
                if batch_count >= batch_size:
                    feed_dict = {input: feature_batch, output: label_batch}
                    sess.run(step, feed_dict=feed_dict)
                    result = sess.run(loss, feed_dict=feed_dict)
                    current_sum += result
                    count += 1
                    print("Batch", count * batch_size, " loss:", result)
                    batch_count = 0
                    feature_batch = []
                    label_batch = []
                else:
                    feature_batch.append(recipes.getNormalizedInputs(recipe.getInputVectorNormalized()))
                    label_batch.append(recipe.getOutputVector())
                    batch_count += 1
            if len(feature_batch) > 0:
                feed_dict = {input: feature_batch, output: label_batch}
                sess.run(step, feed_dict=feed_dict)
                result = sess.run(loss, feed_dict=feed_dict)
                current_sum += result
                count += 1
                print("Batch", count * batch_size, " loss:", result)
            diff = abs(last_loss - current_sum / count)
            last_loss = current_sum / count
            i += 1
            print("Average accuracy for Epoch", i, ":", current_sum / count)


def main():
    layers = input("How many layers?")
    nodes = input("How many nodes per layer?")
    recipeLearner = RecipeLearner(int(layers), int(nodes))
    recipeLearner.train()


if __name__ == '__main__':
    main()