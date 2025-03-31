import tensorflow as tf
import torch
import torch.nn.functional as F

# Enable Distilling 
def distill_model_tflite(teacher_model, student_model, train_data, train_labels):
    # Freeze teacher model
    teacher_model.trainable = False
    
    # Output of teacher and student models
    teacher_output = teacher_model(train_data)
    student_output = student_model(train_data)
    
    # Define distillation loss (KL Divergence)
    distillation_loss = tf.keras.losses.KLDivergence()(teacher_output, student_output)
    
    # Define the optimizer
    optimizer = tf.keras.optimizers.Adam()
    
    # Train the student model
    with tf.GradientTape() as tape:
        loss = distillation_loss + tf.keras.losses.sparse_categorical_crossentropy(train_labels, student_output)
    
    grads = tape.gradient(loss, student_model.trainable_variables)
    optimizer.apply_gradients(zip(grads, student_model.trainable_variables))
    
    return student_model

def distill_model_pytorch(teacher_model, student_model, train_loader, optimizer, temperature=1.0):
    # Set the models to train mode
    teacher_model.train()
    student_model.train()

    # Training loop 
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        
        # Forward pass through teacher and student models
        teacher_logits = teacher_model(inputs)
        student_logits = student_model(inputs)
        
        # Handle potential shape mismatches (e.g., in case of binary classification)
        if len(teacher_logits.shape) == 1:  # If 1D, reshape it
            teacher_logits = teacher_logits.unsqueeze(0)
            student_logits = student_logits.unsqueeze(0)

        if student_logits.size(1) == 1:  # Binary classification case
            student_logits = torch.sigmoid(student_logits)
            teacher_logits = torch.sigmoid(teacher_logits)
            loss = F.binary_cross_entropy(student_logits, teacher_logits)
        else:
            # Knowledge distillation with KL divergence
            loss = F.kl_div(F.log_softmax(student_logits / temperature, dim=-1),
                            F.softmax(teacher_logits / temperature, dim=-1), 
                            reduction='batchmean')
        
        # Backpropagation and optimization
        loss.backward()
        optimizer.step()

    return student_model