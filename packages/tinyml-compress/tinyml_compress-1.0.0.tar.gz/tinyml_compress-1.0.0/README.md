# Model Conversion and Optimization Library (tinyml_compress)

This library provides functions to convert, save, load, distill, prune, and quantize machine learning models for both TensorFlow and PyTorch. It supports model conversion to TFLite and ONNX formats, as well as optimization techniques like distillation, pruning, and quantization.

## Features

- **Model Conversion**:
  - Convert TensorFlow models to TFLite format.
  - Convert PyTorch models to ONNX format.
  
- **Model Optimization**:
  - **Distillation**:
    - Perform knowledge distillation between a teacher and a student model for both TensorFlow and PyTorch.
  - **Pruning**:
    - Apply pruning to TensorFlow and PyTorch models to reduce the number of parameters.
  - **Quantization**:
    - Apply quantization to TensorFlow models to reduce model size and improve inference speed.
    - Apply dynamic quantization to PyTorch models.

- **Model Serialization**:
  - Save and load TensorFlow and PyTorch models to and from disk.

## Installation

### To install this library, you can use the following `pip` command:

pip install tinyML

## Install required dependencies:

pip install -r requirements.txt

## Usage

### Model Conversion

### Convert TensorFlow Model to TFLite
import tensorflow as tf
from model_conversion import convert_to_tflite

Create a simple model
model = tf.keras.Sequential([tf.keras.layers.Dense(10, input_shape=(5,))])

#### Convert to TFLite format
tflite_model = convert_to_tflite(model)


### Convert PyTorch Model to ONNX
import torch
from model_conversion import convert_to_onnx

#### Create a simple model
model = torch.nn.Linear(5, 10)
dummy_input = torch.randn(1, 5)

#### Convert to ONNX format
onnx_path = convert_to_onnx(model, dummy_input, "model.onnx")


## Model Optimization

#### Distillation in TensorFlow
from model_conversion import distill_model_tflite

#### Load teacher model and create student model
teacher_model = tf.keras.models.load_model("teacher_model.h5")
student_model = tf.keras.models.Sequential([tf.keras.layers.Dense(10, input_shape=(5,))])

#### Training data
train_data, train_labels = ...  # Your training data

#### Perform distillation
student_model = distill_model_tflite(teacher_model, student_model, train_data, train_labels)


### Distillation in PyTorch
from model_conversion import distill_model_pytorch

#### Load teacher model and create student model
teacher_model = torch.load("teacher_model.pt")
student_model = torch.nn.Linear(5, 10)

#### Training data loader and optimizer
train_loader = ...  # Your training data loader
optimizer = torch.optim.Adam(student_model.parameters())

#### Perform distillation
student_model = distill_model_pytorch(teacher_model, student_model, train_loader, optimizer)


### Pruning in TensorFlow
from model_conversion import prune_model_tflite

#### Create a simple model
model = tf.keras.Sequential([tf.keras.layers.Dense(10, input_shape=(5,))])

#### Prune the model
pruned_model = prune_model_tflite(model, sparsity=0.5)


### Pruning in PyTorch
from model_conversion import prune_model_pytorch

#### Create a simple model
model = torch.nn.Linear(5, 10)

#### Prune the model
pruned_model = prune_model_pytorch(model, amount=0.3)


### Quantization in TensorFlow
from model_conversion import quantize_model_tflite

#### Create a simple model
model = tf.keras.Sequential([tf.keras.layers.Dense(10, input_shape=(5,))])

#### Quantize the model
quantized_model = quantize_model_tflite(model)


### Quantization in PyTorch
from model_conversion import quantize_model_pytorch

#### Create a simple model
model = torch.nn.Linear(5, 10)

#### Quantize the model
quantized_model = quantize_model_pytorch(model)


## Model Serialization

#### Save a Model
from model_conversion import save_model

### TensorFlow model
model = tf.keras.Sequential([tf.keras.layers.Dense(10, input_shape=(5,))])
save_model(model, "model.h5")

### PyTorch model
import torch
model = torch.nn.Linear(5, 10)
save_model(model, "model.pt")


#### Load a Model
from model_conversion import load_model

#### Load TensorFlow model
tensorflow_model = load_model("model.h5", model_type="tensorflow")

#### Load PyTorch model
pytorch_model = load_model("model.pt", model_type="pytorch", input_shape=(5,))