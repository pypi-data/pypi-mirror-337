from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
import matplotlib.pyplot as plt

def Practical_11():
    print("\n" + "="*50)
    print("AI IN HEALTHCARE: MEDICAL IMAGE ANALYSIS")
    print("="*50 + "\n")
    
    # Load pre-trained VGG16 model
    print("Loading pre-trained VGG16 model...")
    base_model = VGG16(weights='imagenet', include_top=False)
    
    print("\nOriginal VGG16 Architecture (Feature Extraction Part):")
    base_model.summary()
    
    # Adapt for medical imaging (example: chest X-ray classification)
    print("\nAdapting model for healthcare application...")
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(2, activation='softmax')(x)  # Binary classification
    
    # Create final model
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Freeze convolutional layers
    for layer in base_model.layers:
        layer.trainable = False
    
    print("\nModified Architecture for Medical Imaging:")
    model.summary()
    
    # Visualize model adaptation
    plt.figure(figsize=(12, 6))
    
    # Original vs modified architecture
    plt.subplot(1, 2, 1)
    plt.title("Original VGG16")
    plt.text(0.5, 0.5, "VGG16 Base Architecture\n(Feature Extraction Layers)", ha='center', va='center')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.title("Modified for Healthcare")
    plt.text(0.5, 0.5, 
        "Added:\n- Global Average Pooling\n- Dense Layers\n- Disease Classification Head", 
        ha='center', va='center')
    plt.axis('off')
    
    plt.suptitle("Transfer Learning for Medical Imaging", y=1.05)
    plt.tight_layout()
    plt.show()
    
    # Healthcare-specific implementation details
    print("\nHealthcare Implementation Considerations:")
    print("- Preprocessing medical images (windowing, normalization)")
    print("- Handling class imbalance in medical data")
    print("- Integrating clinical metadata")
    print("- Explainability for clinical decision support")
    
    # Example medical image processing
    print("\nExample Medical Image Processing Pipeline:")
    steps = [
        "1. DICOM/NIfTI Image Loading",
        "2. Intensity Normalization (e.g., HU values for CT)",
        "3. Anatomical Region Cropping",
        "4. Data Augmentation (flips, rotations)",
        "5. Transfer Learning with Frozen Base",
        "6. Fine-tuning Selected Layers"
    ]
    print("\n".join(steps))
    
    # Ethical considerations
    print("\nHealthcare AI Ethics:")
    print("- Patient privacy (HIPAA/GDPR compliance)")
    print("- Model transparency for clinical validation")
    print("- Guarding against hidden biases")
    print("- Clinical impact assessment")
    
    return model

# Call the function with:
# medical_model = Practical_11()