import unittest
import tensorflow as tf
import torch
from tinyml_compress.distill import distill_model_tflite, distill_model_pytorch

class TestDistillation(unittest.TestCase):

    def test_distill_tflite(self):
        teacher_model = tf.keras.Sequential([tf.keras.layers.Dense(10, activation='softmax', input_shape=(5,))])
        student_model = tf.keras.Sequential([tf.keras.layers.Dense(10, activation='softmax', input_shape=(5,))])
        train_data = tf.random.uniform((10, 5))
        train_labels = tf.random.uniform((10, 10))

        distilled_model = distill_model_tflite(teacher_model, student_model, train_data, train_labels)
        self.assertTrue(isinstance(distilled_model, tf.keras.Model))

    def test_distill_pytorch(self):
        teacher_model = torch.nn.Linear(5, 10)
        student_model = torch.nn.Linear(5, 10)
        train_loader = [ (torch.randn(5), torch.randn(10)) for _ in range(3)]
        optimizer = torch.optim.Adam(student_model.parameters())

        distilled_model = distill_model_pytorch(teacher_model, student_model, train_loader, optimizer)
        self.assertTrue(isinstance(distilled_model, torch.nn.Module))

if __name__ == '__main__':
    unittest.main()