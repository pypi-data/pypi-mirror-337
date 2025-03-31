import unittest
import tensorflow as tf
import torch
from tinyml_compress.quant import quantize_model_tflite, quantize_model_pytorch

class TestQuantization(unittest.TestCase):

    def test_quantize_tflite(self):
        model = tf.keras.Sequential([tf.keras.layers.Dense(10, input_shape=(5,))])
        quantized_model = quantize_model_tflite(model)
        self.assertTrue(isinstance(quantized_model, bytes))

    def test_quantize_pytorch(self):
        model = torch.nn.Linear(5, 10)
        quantized_model = quantize_model_pytorch(model)
        self.assertTrue(isinstance(quantized_model, torch.nn.Linear))  
        self.assertTrue(hasattr(quantized_model, 'weight')) 

if __name__ == '__main__':
    unittest.main()