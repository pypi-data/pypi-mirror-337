import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def Practical_2():
    # Generating data
    X = np.random.rand(100, 1) * 10
    y = 2.5 * X + np.random.randn(100, 1) * 2

    # Splitting dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Training the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predicting
    y_pred = model.predict(X_test)

    # Plotting results
    plt.figure(figsize=(8, 6))
    plt.scatter(X_test, y_test, color="blue", label="Actual")
    plt.plot(X_test, y_pred, color="red", label="Predicted")
    plt.title("Linear Regression Example")
    plt.xlabel("X")
    plt.ylabel("y")
    plt.legend()
    plt.show()

    # Print model coefficients
    print(f"Model coefficients:")
    print(f"Slope (coefficient): {model.coef_[0][0]:.2f}")
    print(f"Intercept: {model.intercept_[0]:.2f}")

# You can call the function like this:
# Practical_2()