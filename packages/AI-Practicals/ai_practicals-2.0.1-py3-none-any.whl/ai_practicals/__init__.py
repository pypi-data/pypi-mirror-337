"""
AI Practical Implementations Package

A comprehensive collection of ready-to-run AI/ML implementations covering:
- Fundamental machine learning algorithms
- Deep learning models (CNNs, GANs, Transformers)
- Natural Language Processing (NLP) techniques
- Computer vision applications
- Reinforcement learning demos
- AI ethics case studies
- Healthcare AI applications
- Business analytics implementations
- Robotics simulations
"""

__version__ = "2.0.0"
__author__ = "Shreeyansh Pashine"
__email__ = "Shreeyanshpashine@gmail.com"
__license__ = "MIT"
__url__ = "https://github.com/Shreeyanshpashin/ai-practicals"

# Import all practical modules
from .practical_1 import Practical_1 as LinearAlgebraDemo
from .practical_2 import Practical_2 as LinearRegressionDemo
from .practical_3 import Practical_3 as NeuralNetworkXORDemo
from .practical_4 import Practical_4 as MNISTCNNDemo
from .practical_5 import Practical_5 as NLPDemo
from .practical_6 import Practical_6 as QLearningDemo
from .practical_7 import Practical_7 as GANDemo
from .practical_8 import Practical_8 as TransferLearningDemo
from .practical_9 import Practical_9 as ExplainableAIDemo
from .practical_10 import Practical_10 as AIEthicsDemo
from .practical_11 import Practical_11 as HealthcareAIDemo
from .practical_12 import Practical_12 as TransformersDemo
from .practical_13 import Practical_13 as BusinessAIDemo
from .practical_14 import Practical_14 as RoboticsAIDemo

# Define public API
__all__ = [
    'LinearAlgebraDemo',
    'LinearRegressionDemo',
    'NeuralNetworkXORDemo',
    'MNISTCNNDemo',
    'NLPDemo',
    'QLearningDemo',
    'GANDemo',
    'TransferLearningDemo',
    'ExplainableAIDemo',
    'AIEthicsDemo',
    'HealthcareAIDemo',
    'TransformersDemo',
    'BusinessAIDemo',
    'RoboticsAIDemo'
]

# Package initialization
def get_practicals():
    """Return dictionary of all available practicals with descriptions"""
    return {
        'LinearAlgebraDemo': "Basic linear algebra operations with NumPy",
        'LinearRegressionDemo': "Linear regression implementation with scikit-learn",
        'NeuralNetworkXORDemo': "Neural network solving XOR problem",
        'MNISTCNNDemo': "CNN for MNIST digit classification",
        'NLPDemo': "Natural Language Processing basics with NLTK",
        'QLearningDemo': "Reinforcement learning with Q-Learning",
        'GANDemo': "Generative Adversarial Network implementation",
        'TransferLearningDemo': "Transfer learning with ResNet18",
        'ExplainableAIDemo': "Model interpretability with SHAP values",
        'AIEthicsDemo': "Case study on AI ethics and bias",
        'HealthcareAIDemo': "Medical image analysis with CNNs",
        'TransformersDemo': "Text generation with GPT-2",
        'BusinessAIDemo': "Customer segmentation with K-Means",
        'RoboticsAIDemo': "Path planning simulation for robotics"
    }

def version_info():
    """Print package version information"""
    print(f"AI Practicals v{__version__}")
    print(f"Author: {__author__} ({__email__})")
    print(f"License: {__license__}")
    print(f"Documentation: {__url__}")

# Display version info when imported
version_info()