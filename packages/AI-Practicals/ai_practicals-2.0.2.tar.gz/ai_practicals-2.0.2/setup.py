from setuptools import setup, find_packages
import os

# Read long description from README.md
def get_long_description():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "A collection of practical AI/ML implementations"

# Package configuration
setup(
    name="AI_Practicals",
    version="2.0.2",  # Consider using a dynamic version from __init__.py
    author="Shreeyansh Pashine",
    author_email="Shreeyanshpashine@gmail.com",
    description="A collection of practical AI/ML implementations",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/Shreeyanshpashin/ai-practicals",
    project_urls={
        "Bug Tracker": "https://github.com/Shreeyanshpashin/ai-practicals/issues",
        "Source Code": "https://github.com/Shreeyanshpashin/ai-practicals",
    },
    packages=find_packages(include=["ai_practicals", "ai_practicals.*"]),
    package_dir={"": "."},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
        "matplotlib>=3.3.0",
        "scikit-learn>=0.24.0",
        "tensorflow>=2.5.0; sys_platform != 'win32'",  # Windows might need special handling
        "torch>=1.8.0",
        "nltk>=3.6.0",
        "pandas>=1.2.0",
        "shap>=0.39.0",
        "xgboost>=1.4.0",
        "transformers>=4.0.0",
        "ipython>=7.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0",
            "flake8>=3.9.0",
            "mypy>=0.900",
            "pydocstyle>=6.0.0",
            "twine>=3.4.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
            "myst-parser>=0.15.0",
        ],
        "full": [
            "opencv-python>=4.5.0",
            "seaborn>=0.11.0",
            "plotly>=5.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "ai-practical=ai_practicals.cli:main",
        ],
    },
    package_data={
        "ai_practicals": ["data/*.csv", "data/*.json", "data/*.pkl"],
    },
    include_package_data=True,
    license="MIT",
    keywords=[
        "machine-learning",
        "artificial-intelligence",
        "deep-learning",
        "education",
        "examples",
        "practical-ai",
    ],
    zip_safe=False,
)