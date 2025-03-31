import tensorflow_model_optimization as tfmot 
import torch.nn.utils.prune as prune
import torch 

# Enable Pruning 

def prune_model_tflite(model, sparsity=0.5):
    pruning_schedule = tfmot.sparsity.keras.PolynomialDecay(
        initial_sparsity=0.0, final_sparsity=sparsity, begin_step=0, end_step=1000)
    pruned_model = tfmot.sparsity.keras.prune_low_magnitude(model, pruning_schedule)
    return pruned_model

def prune_model_pytorch(model, amount=0.3):
    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Linear):  # Prune Linear layers
            prune.l1_unstructured(module, name='weight', amount=amount)
    return model