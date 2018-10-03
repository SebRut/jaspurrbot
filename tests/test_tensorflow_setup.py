import unittest
import os
from textgenrnn import textgenrnn
import tensorflow as tf
from keras.backend import clear_session

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

global graph
clear_session()
graph = tf.get_default_graph()


class TensorflowTestMethods(unittest.TestCase):
    def test_textgenrnn_basic(self):
        textgen = textgenrnn(weights_path=os.path.join('model', 'jodler_weights.hdf5'),
                             vocab_path=os.path.join('model', 'jodler_vocab.json'),
                             config_path=os.path.join('model', 'jodler_config.json'))
        with graph.as_default():
            message = textgen.generate(1, return_as_list=True)[0]
        print(message)
        self.assertIsNot("", message)


if __name__ == '__main__':
    unittest.main()