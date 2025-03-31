import unittest
import tensorflow as tf
import torch
import torch.nn as nn
import os
import tempfile
from tinyml_compress import convert_to_tflite, convert_to_onnx, save_model, load_model, convert_model  # Import your functions



class SimpleNN(nn.Module):
    def __init__(self, input_size=5, num_classes=2):
        super(SimpleNN, self).__init__()
        self.fc = nn.Linear(input_size, num_classes)

    def forward(self, x):
        return self.fc(x)


class TestModelConversion(unittest.TestCase):

    def setUp(self):
        """Set up for each test"""
        # TensorFlow model setup
        self.tf_model = tf.keras.Sequential([
            tf.keras.layers.Dense(10, input_shape=(5,)),
            tf.keras.layers.Dense(2)
        ])

        # PyTorch model setup
        self.pt_model = SimpleNN()  # Now SimpleNN is accessible here

        # Dummy input for ONNX export
        self.dummy_input = torch.randn(1, 5)

    def test_convert_to_tflite(self):
        """Test TensorFlow model conversion to TFLite"""
        tflite_model = convert_to_tflite(self.tf_model)
        self.assertIsInstance(tflite_model, bytes)  # TFLite model is byte data
        self.assertGreater(len(tflite_model), 0)  # Ensure model is not empty

    def test_convert_to_onnx(self):
        """Test PyTorch model conversion to ONNX"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".onnx") as onnx_file:
            onnx_path = onnx_file.name  # Ensure the temp file has the correct .onnx extension
        
        # Convert model and store the returned file path
        onnx_model = convert_to_onnx(self.pt_model, self.dummy_input, onnx_path)

        # Ensure the file path returned matches the expected .onnx file
        self.assertEqual(onnx_model, onnx_path)
        self.assertTrue(os.path.exists(onnx_path)) 

    def test_save_and_load_tensorflow_model(self):
        """Test saving and loading a TensorFlow model"""
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = os.path.join(temp_dir, "tf_model.h5")
            save_model(self.tf_model, model_path)
            loaded_model = load_model(model_path)
            self.assertIsInstance(loaded_model, tf.keras.Model)

    def test_save_and_load_pytorch_model(self):
        """Test saving and loading a PyTorch model"""
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = os.path.join(temp_dir, "pt_model.pth")
            save_model(self.pt_model, model_path)
            
            # Provide the required arguments for load_model
            loaded_model = load_model(model_path, model_class=SimpleNN, input_shape=(5,), num_classes=2)
            
            self.assertIsInstance(loaded_model, torch.nn.Module)

    def test_convert_model_to_onnx(self):
        """Test general model conversion to ONNX"""
        with tempfile.NamedTemporaryFile(delete=False) as onnx_file:
            onnx_path = onnx_file.name
        onnx_model = convert_model(self.pt_model, self.dummy_input, target_format="onnx", output_path=onnx_path)
        self.assertEqual(onnx_model, onnx_path + '.onnx')  
        self.assertTrue(os.path.exists(onnx_path))  # Ensure the ONNX file is saved
        os.remove(onnx_path)

    def test_convert_model_to_tflite(self):
        """Test general model conversion to TFLite"""
        tflite_model = convert_model(self.tf_model, target_format="tflite", output_path="tflite_model")
        self.assertIsInstance(tflite_model, bytes)
        self.assertGreater(len(tflite_model), 0)  # Ensure the model is not empty

    def test_invalid_conversion(self):
        """Test invalid model conversion"""
        with self.assertRaises(ValueError):
            convert_model(self.pt_model, target_format="tflite", output_path="invalid_conversion")

        with self.assertRaises(ValueError):
            convert_model(self.tf_model, target_format="onnx", output_path="invalid_conversion")

    def test_invalid_model_type_for_conversion(self):
        """Test invalid model type for conversion"""
        with self.assertRaises(TypeError):
            convert_to_tflite(self.pt_model)  # PyTorch model cannot be converted to TFLite

        with self.assertRaises(TypeError):
            convert_to_onnx(self.tf_model, self.dummy_input)  # TensorFlow model cannot be converted to ONNX


if __name__ == '__main__':
    unittest.main()