import shap
import xgboost
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd

def Practical_9():
    print("\n" + "="*50)
    print("EXPLAINABLE AI WITH SHAP VALUES")
    print("="*50 + "\n")
    
    # Load California housing dataset
    data = fetch_california_housing()
    X, y = data.data, data.target
    feature_names = data.feature_names
    
    # Split into train-test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Dataset Overview:")
    print(f"Features: {feature_names}")
    print(f"Training samples: {X_train.shape[0]}")
    print(f"Test samples: {X_test.shape[0]}\n")
    
    # Train XGBoost model
    print("Training XGBoost model...")
    model = xgboost.XGBRegressor(random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"\nModel Performance:")
    print(f"Training R²: {train_score:.3f}")
    print(f"Test R²: {test_score:.3f}")
    
    # SHAP explanation
    print("\nComputing SHAP values...")
    explainer = shap.Explainer(model, X_train, feature_names=feature_names)
    shap_values = explainer(X_test)
    
    # Create figure for all visualizations
    plt.figure(figsize=(15, 10))
    
    # Waterfall plot for first prediction
    plt.subplot(2, 2, 1)
    shap.plots.waterfall(shap_values[0], show=False)
    plt.title("Waterfall Plot for First Prediction")
    
    # Force plot for first prediction
    plt.subplot(2, 2, 2)
    shap.plots.force(shap_values[0], show=False, matplotlib=True)
    plt.title("Force Plot for First Prediction")
    
    # Feature importance
    plt.subplot(2, 2, 3)
    shap.plots.bar(shap_values, show=False)
    plt.title("Global Feature Importance")
    
    # Summary plot
    plt.subplot(2, 2, 4)
    shap.summary_plot(shap_values, X_test, feature_names=feature_names, show=False)
    plt.title("Feature Impact Summary")
    
    plt.tight_layout()
    plt.show()
    
    # Print interpretation guide
    print("\nSHAP Value Interpretation:")
    print("- Positive SHAP value: Feature increases prediction")
    print("- Negative SHAP value: Feature decreases prediction")
    print("- Magnitude shows strength of effect")
    print("\nKey Insights:")
    print("1. See which features drive individual predictions (waterfall/force plots)")
    print("2. Understand global feature importance (bar plot)")
    print("3. View feature impact distribution (summary plot)")
    
    # Return SHAP values for further analysis
    return shap_values

# Call the function with:
# shap_values = Practical_9()