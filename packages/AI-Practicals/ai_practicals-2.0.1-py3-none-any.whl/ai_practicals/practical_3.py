import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

def Practical_3():
    # XOR dataset
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float32)
    y = np.array([[0], [1], [1], [0]], dtype=np.float32)
    
    # Building the model
    model = keras.Sequential([
        keras.layers.Dense(4, activation="relu", input_shape=(2,)),
        keras.layers.Dense(1, activation="sigmoid")
    ])
    
    # Compile and train
    model.compile(optimizer="adam", 
                 loss="binary_crossentropy", 
                 metrics=["accuracy"])
    
    print("Training neural network for XOR problem...")
    history = model.fit(X, y, epochs=500, verbose=0)
    
    # Evaluate
    predictions = model.predict(X)
    print("\nPredictions:")
    for i, (input_data, true_val, pred) in enumerate(zip(X, y, predictions)):
        print(f"Input: {input_data} | True: {true_val[0]} | Predicted: {pred[0]:.4f}")
    
    # Plot training history
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'])
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    
    plt.tight_layout()
    plt.show()

# Call the function with:
# Practical_3()