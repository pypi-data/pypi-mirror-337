import tensorflow as tf
import torch
import torch.onnx
import os

# Convert model to TFLite (for TensorFlow models)
def convert_to_tflite(model):
    if isinstance(model, tf.keras.Model):
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        tflite_model = converter.convert()
        return tflite_model
    else:
        raise TypeError("Only TensorFlow models can be converted to TFLite")


# Convert model to ONNX (for PyTorch models)
def convert_to_onnx(model, dummy_input, onnx_path="model.onnx"):
    if isinstance(model, torch.nn.Module):
        model.eval()
        torch.onnx.export(model, dummy_input, onnx_path, verbose=True)
        return onnx_path
    else:
        raise TypeError("Only PyTorch models can be converted to ONNX")


# Save model (supports TensorFlow and PyTorch)
def save_model(model, path):
    if isinstance(model, tf.keras.Model):
        model.save(path)  # Save TensorFlow model
    elif isinstance(model, torch.nn.Module):
        torch.save(model.state_dict(), path)  # Save PyTorch model
    else:
        raise TypeError("Unsupported model type. Supported types: TensorFlow, PyTorch")


# Load model (supports TensorFlow and PyTorch)
def load_model(path, input_shape=None, num_classes=None, model_class=None):
    _, ext = os.path.splitext(path)

    if ext == '.h5':  # TensorFlow model
        return tf.keras.models.load_model(path)

    elif ext in ['.pt', '.pth']:  # PyTorch model
        if input_shape is None or num_classes is None or model_class is None:
            raise ValueError("For PyTorch, input_shape, num_classes, and model_class must be provided.")

        # Create an instance of the model class dynamically
        model = model_class(*input_shape, num_classes)

        # Load model weights
        model.load_state_dict(torch.load(path))
        model.eval()  # Set to evaluation mode
        return model

    else:
        raise ValueError(f"Unsupported model format: {ext}. Supported formats: .h5 (TensorFlow), .pt/.pth (PyTorch)")


# General function for model conversion to multiple formats (TFLite, ONNX)
def convert_model(model, dummy_input=None, target_format='onnx', output_path="converted_model"):
    """Converts the model to the specified format ('onnx', 'tflite')"""
    if target_format == 'onnx' and isinstance(model, torch.nn.Module):
        return convert_to_onnx(model, dummy_input, output_path + ".onnx")
    
    elif target_format == 'tflite' and isinstance(model, tf.keras.Model):
        return convert_to_tflite(model)
    
    else:
        raise ValueError(f"Invalid conversion request: Cannot convert {type(model)} to {target_format}.")
    
