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
    nodes = 30

    def __init__(self):
        input = tf.placeholder(tf.float32, [None, self.input_size])
        output = tf.placeholder(tf.float32, [None, self.output_size])

        # Setup weights and layers
        w0 = tf.Variable(tf.truncated_normal([self.input_size, self.nodes]))
        layer0 = tf.Variable(tf.truncated_normal([1, self.nodes]))
        w1 = tf.Variable(tf.truncated_normal([self.nodes, self.output_size]))
        layer1 = tf.Variable(tf.truncated_normal([1, self.output_size]))

        # Run forward step
        z0 = tf.add(tf.matmul(input, w0), layer0)
        forward0 = sigma(z0)
        z1 = tf.add(tf.matmul(forward0, w1), layer1)
        forward1 = sigma(z1)

        # Back propagate
        diff = tf.subtract(forward1, output)
        cost = tf.multiply(diff, diff)
        step = tf.train.GradientDescentOptimizer(0.1).minimize(cost)

        loss = tf.reduce_sum(tf.abs(output - forward1))

        sess = tf.InteractiveSession()
        sess.run(tf.global_variables_initializer())

        recipes = RecipeDatabase()
        for i in range(10):
            current_sum = 0
            count = 0
            batch_size = 10
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
                    batch_count = 0
                    feature_batch = []
                    label_batch = []
                else:
                    feature_batch.append(recipe.getInputVectorNormalized())
                    label_batch.append(recipe.getOutputVector())
                    batch_count += 1
            if len(feature_batch) > 0:
                feed_dict = {input: feature_batch, output: label_batch}
                sess.run(step, feed_dict=feed_dict)
                result = sess.run(loss, feed_dict=feed_dict)
                current_sum += result
                count += 1
            print("Average accuracy for Epoch", i, ":", current_sum / count)


def main():
    recipeLearner = RecipeLearner()


if __name__ == '__main__':
    main()