import tensorflow as tf
import numpy as np
import os
from pymongo import MongoClient
from tqdm import tqdm, trange


class RecipeLearner:
    input_size = 10
    output_size = 5
    epochs = 100
    model_directory = './learned_model'

    def __init__(self):
        self.sess = tf.Session()
        self.x = tf.placeholder(tf.float64, [1, self.input_size], name='x')
        layer0 = tf.layers.dense(self.x, 16, activation=tf.nn.relu, name='layer0')
        layer1 = tf.layers.dense(layer0, 12, activation=tf.nn.relu, name='layer1')
        layer2 = tf.layers.dense(layer1, 8, activation=tf.nn.relu, name='layer2')
        layer3 = tf.layers.dense(layer2, 5, activation=tf.nn.relu, name='layer3')
        self.result = layer3
        self.loss = tf.reduce_sum(tf.abs(self.x - self.result), name='loss')
        self.train = tf.train.AdamOptimizer().minimize(self.loss, name='train')
        tf.add_to_collection('x', self.x)
        tf.add_to_collection('result', self.result)
        tf.add_to_collection('loss', self.loss)
        tf.add_to_collection('train', self.train)
        self.saver = tf.train.Saver()

    def start_training(self, load_existing_model=True):
        if load_existing_model and os.path.exists(self.model_directory):
            self.load_trained_model()
        else:
            self.sess.run(tf.global_variables_initializer())
        epoch_iterator = trange(self.epochs)
        for e in epoch_iterator:
            current_sum = 0
            count = 0
            #try:
                #for recipe in batch:
                    #try:
                        #feed_dict = {self.x: recipe}
                        #loss, _ = self.sess.run([self.loss, self.train], feed_dict=feed_dict)
                        #count += 1
                        #current_sum += loss
                    #except Exception:
                        #continue
            #except Exception:
                #continue
            #finally:
                #self.save_trained_model()
                #epoch_iterator.set_description('Epoch {} average training loss: {}'.format(e, current_sum / count))

    def save_trained_model(self):
        self.saver.save(self.sess, os.path.join(self.model_directory, 'model'))

    def load_trained_model(self):
        self.saver.restore(self.sess, tf.train.latest_checkpoint(self.model_directory))


def main():
    recipeLearner = RecipeLearner()
    recipeLearner.start_training()


if __name__ == '__main__':
    main()
