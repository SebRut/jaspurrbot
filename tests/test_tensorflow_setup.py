import unittest
import os
from textgenrnn import textgenrnn


class TensorflowTestMethods(unittest.TestCase):
    def test_textgenrnn_basic(self):
        textgen = textgenrnn(weights_path=os.path.join('model', 'jodler_weights.hdf5'),
                             vocab_path=os.path.join('model', 'jodler_vocab.json'),
                             config_path=os.path.join('model', 'jodler_config.json'))
        message = textgen.generate(1, return_as_list=True)[0]
        self.assertIsNot("", message)


if __name__ == '__main__':
    unittest.main()