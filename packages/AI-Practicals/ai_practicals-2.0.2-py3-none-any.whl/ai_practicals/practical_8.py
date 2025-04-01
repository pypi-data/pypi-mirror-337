import torch
import torchvision.models as models
from torchsummary import summary
import matplotlib.pyplot as plt

def Practical_8():
    print("\n" + "="*50)
    print("TRANSFER LEARNING WITH RESNET18")
    print("="*50 + "\n")
    
    # Load pre-trained ResNet18 model
    model = models.resnet18(pretrained=True)
    
    print("Original ResNet18 Architecture:")
    print(model)
    print("\nTotal Parameters:", sum(p.numel() for p in model.parameters()))
    print("Trainable Parameters (before freezing):", 
          sum(p.numel() for p in model.parameters() if p.requires_grad))
    
    # Freeze all layers
    for param in model.parameters():
        param.requires_grad = False
    
    # Modify the final layer for 10-class classification
    num_features = model.fc.in_features
    model.fc = torch.nn.Linear(num_features, 10)
    
    print("\nModified Model Architecture:")
    print(model)
    print("\nTotal Parameters:", sum(p.numel() for p in model.parameters()))
    print("Trainable Parameters (after freezing):", 
          sum(p.numel() for p in model.parameters() if p.requires_grad))
    
    # Visualize model architecture
    try:
        # Try to get model summary (works better with GPU)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        summary(model.to(device), input_size=(3, 224, 224))
    except:
        print("\nNote: Install torchsummary for detailed layer-wise summary")
        print("pip install torchsummary")
    
    # Plot parameter information
    plt.figure(figsize=(10, 5))
    
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    frozen_params = total_params - trainable_params
    
    plt.bar(['Total', 'Trainable', 'Frozen'], 
            [total_params, trainable_params, frozen_params],
            color=['blue', 'green', 'red'])
    plt.title('Model Parameters')
    plt.ylabel('Number of Parameters')
    plt.yscale('log')
    plt.grid(True, which="both", ls="--")
    
    plt.tight_layout()
    plt.show()
    
    print("\nTransfer Learning Process:")
    print("1. Start with pre-trained model (trained on ImageNet)")
    print("2. Freeze all existing layers to preserve learned features")
    print("3. Replace and retrain final layer for new task (10-class classification)")
    print("4. Optionally fine-tune some layers if needed")
    
    print("\nKey Benefits:")
    print("- Leverages learned feature representations")
    print("- Requires less data than training from scratch")
    print("- Faster training (only final layer trains initially)")

# Call the function with:
# Practical_8()