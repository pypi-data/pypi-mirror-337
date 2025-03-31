import unittest
import tensorflow as tf
import torch
from tinyml_compress.prune import prune_model_tflite, prune_model_pytorch

class TestPruning(unittest.TestCase):

    def test_prune_tflite(self):
        model = tf.keras.Sequential([tf.keras.layers.Dense(10, input_shape=(5,))])
        pruned_model = prune_model_tflite(model, sparsity=0.5)
        self.assertTrue(isinstance(pruned_model, tf.keras.Model))

    def test_prune_pytorch(self):
        model = torch.nn.Linear(5, 10)
        pruned_model = prune_model_pytorch(model, amount=0.3)
        self.assertTrue(isinstance(pruned_model, torch.nn.Module))

if __name__ == '__main__':
    unittest.main()