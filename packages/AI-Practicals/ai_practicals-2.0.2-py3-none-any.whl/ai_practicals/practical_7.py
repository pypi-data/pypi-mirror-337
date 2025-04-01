import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np

def Practical_7():
    # Set random seed for reproducibility
    torch.manual_seed(42)
    
    print("\n" + "="*50)
    print("GENERATIVE ADVERSARIAL NETWORK IMPLEMENTATION")
    print("="*50 + "\n")
    
    # Generator definition
    class Generator(nn.Module):
        def __init__(self, latent_dim=100):
            super(Generator, self).__init__()
            self.model = nn.Sequential(
                nn.Linear(latent_dim, 256),
                nn.LeakyReLU(0.2),
                nn.Linear(256, 512),
                nn.LeakyReLU(0.2),
                nn.Linear(512, 784),  # 28x28 for MNIST-like images
                nn.Tanh()  # Output between -1 and 1
            )
            
        def forward(self, z):
            return self.model(z)
    
    # Create generator instance
    latent_dim = 100
    gen = Generator(latent_dim)
    
    print("Generator Architecture:")
    print(gen)
    print("\nGenerator Parameters:")
    print(f"Input dimension: {latent_dim}")
    print(f"Output dimension: 784 (28x28 image)")
    
    # Generate sample noise
    num_samples = 1
    noise = torch.randn(num_samples, latent_dim)
    
    # Generate fake image
    with torch.no_grad():
        fake_image = gen(noise).detach()
    
    # Reshape and visualize
    fake_image = fake_image.view(-1, 28, 28).numpy()
    
    plt.figure(figsize=(8, 8))
    plt.imshow(fake_image[0], cmap='gray')
    plt.title("Generated Image from Random Noise")
    plt.colorbar()
    plt.axis('off')
    plt.show()
    
    # Print additional information
    print("\nTraining Process Overview:")
    print("1. Generator creates fake images from random noise")
    print("2. Discriminator learns to distinguish real vs fake images")
    print("3. Both networks compete in a minimax game")
    print("4. Goal: Generator produces realistic images that fool discriminator")
    
    print("\nKey Components:")
    print("- Generator: Transforms noise to data space")
    print("- Discriminator: Classifies real vs generated data")
    print("- Loss Functions: Binary cross-entropy")
    print("- Optimizers: Typically Adam for both networks")

# Call the function with:
# Practical_7()