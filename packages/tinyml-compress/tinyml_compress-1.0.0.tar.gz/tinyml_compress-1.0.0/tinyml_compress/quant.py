import tensorflow as tf
import torch
import torch.quantization

# Enable Quantization

def quantize_model_tflite(model):
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]  
    tflite_model = converter.convert()
    return tflite_model

def quantize_model_pytorch(model):
    model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
    model = torch.quantization.prepare(model)
    model = torch.quantization.convert(model)
    return model
