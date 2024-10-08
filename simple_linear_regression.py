# -*- coding: utf-8 -*-
"""Simple Linear Regression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kf6VTNFwNvh9qLaDgeFqH8TPWujeDhp0
"""

import numpy as np
import matplotlib.pyplot as plt

# Dataset
x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
y = np.array([1, 3, 2, 5, 7, 8, 8, 9, 10, 12])

# Add a column of ones to x for the intercept term
X = np.c_[np.ones(x.shape[0]), x]

# Analytical Solution using Normal Equation
theta_analytic = np.linalg.inv(X.T @ X) @ X.T @ y
y_pred_analytic = X @ theta_analytic

# Sum Squared Error (SSE) for analytical solution
sse_analytic = np.sum((y - y_pred_analytic)**2)

# R^2 value for analytical solution
ss_total = np.sum((y - np.mean(y))**2)
r2_analytic = 1 - (sse_analytic / ss_total)

print(f"Analytical Solution - Coefficients: {theta_analytic}")
print(f"SSE (Analytical): {sse_analytic}")
print(f"R² (Analytical): {r2_analytic}")

# Full-batch Gradient Descent
def gradient_descent(X, y, learning_rate=0.01, epochs=1000, tolerance=1e-6):
    m = len(y)
    theta = np.random.randn(2)
    prev_sse = float('inf')

    for epoch in range(epochs):
        y_pred = X @ theta
        error = y_pred - y
        sse = np.sum(error**2)

        if abs(prev_sse - sse) < tolerance:
            break

        gradient = (2/m) * (X.T @ error)
        theta = theta - learning_rate * gradient
        prev_sse = sse

    return theta, sse

theta_batch, sse_batch = gradient_descent(X, y)
y_pred_batch = X @ theta_batch
r2_batch = 1 - (sse_batch / ss_total)

print(f"Full-Batch Gradient Descent - Coefficients: {theta_batch}")
print(f"SSE (Full-Batch): {sse_batch}")
print(f"R² (Full-Batch): {r2_batch}")

# Stochastic Gradient Descent
def stochastic_gradient_descent(X, y, learning_rate=0.01, epochs=1000, tolerance=1e-6):
    m = len(y)
    theta = np.random.randn(2)
    prev_sse = float('inf')

    for epoch in range(epochs):
        for i in range(m):
            rand_index = np.random.randint(m)
            xi = X[rand_index:rand_index+1]
            yi = y[rand_index:rand_index+1]
            y_pred = xi @ theta
            error = y_pred - yi
            sse = np.sum((X @ theta - y)**2)

            if abs(prev_sse - sse) < tolerance:
                break

            gradient = 2 * xi.T @ error
            theta = theta - learning_rate * gradient
            prev_sse = sse

    return theta, sse

theta_stochastic, sse_stochastic = stochastic_gradient_descent(X, y)
y_pred_stochastic = X @ theta_stochastic
r2_stochastic = 1 - (sse_stochastic / ss_total)

print(f"Stochastic Gradient Descent - Coefficients: {theta_stochastic}")
print(f"SSE (Stochastic): {sse_stochastic}")
print(f"R² (Stochastic): {r2_stochastic}")

# Plotting the regression lines
plt.scatter(x, y, color='blue', label='Data Points')
plt.plot(x, y_pred_analytic, color='green', label='Analytical Solution')
plt.plot(x, y_pred_batch, color='red', label='Full-Batch GD')
plt.plot(x, y_pred_stochastic, color='orange', label='Stochastic GD')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
# import matplotlib.pyplot as plt

# Load the California housing dataset instead of the Boston dataset
from sklearn.datasets import fetch_california_housing
housing = fetch_california_housing()
df = pd.DataFrame(housing.data, columns=housing.feature_names)
df['PRICE'] = housing.target

X = df.drop("PRICE", axis=1)
y = df["PRICE"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.4, random_state=1)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R² Score: {r2}")