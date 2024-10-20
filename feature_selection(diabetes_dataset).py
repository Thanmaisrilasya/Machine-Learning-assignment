# -*- coding: utf-8 -*-
"""feature_selection(diabetes_dataset).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TMiYGO_-ewBmJWQwJ_VN0qoCYVaCbn51
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE, SelectKBest, VarianceThreshold
from sklearn.metrics import accuracy_score

# Path to the CSV file on your system
csv_path = 'diabetes.csv'

# Load the data into a pandas DataFrame
data = pd.read_csv(csv_path)

# Show the initial rows of the dataset
print(data.head())

# Calculate the percentage of missing values for each column
null_percentage = data.isnull().sum() / len(data) * 100
print(null_percentage)

# Identify columns where the percentage of missing values is greater than 30%
columns_to_drop = null_percentage[null_percentage > 30].index

# Drop these columns and display the updated DataFrame
filtered_data = data.drop(columns=columns_to_drop)
print(filtered_data.head())

# Separate the features (X) and the target variable (y) from the dataset
features = filtered_data.drop(columns=['Outcome'])  # Assuming 'Outcome' is the target column
target = filtered_data['Outcome']

# Display the features after removing the target column
print("\nFeatures (X):")
print(features)

def low_variance_filter(data, threshold=0.01):
    # Initialize the VarianceThreshold filter
    variance_filter = VarianceThreshold(threshold=threshold)
    # Apply the filter to reduce the dataset
    reduced_data = variance_filter.fit_transform(data)
    return reduced_data

# Apply the low variance filter and check performance
filtered_features = low_variance_filter(features)

# Split the data for the model using the filtered dataset
X_train, X_test, y_train, y_test = train_test_split(filtered_features, target, test_size=0.2, random_state=42)

# Initialize and train a RandomForest model
random_forest_model = RandomForestClassifier(random_state=42)
random_forest_model.fit(X_train, y_train)

# Predict and calculate accuracy
predictions = random_forest_model.predict(X_test)
accuracy_filtered = accuracy_score(y_test, predictions)

print(f"Accuracy after applying the low variance filter: {accuracy_filtered:.2f}")

# Compute the correlation matrix for the features
corr_matrix = features.corr()

# Display the correlation matrix
print("Correlation Matrix:")
print(corr_matrix)

# Visualize the correlation matrix using a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix of Features")
plt.show()

# Function to eliminate highly correlated features
def drop_high_correlation(data, threshold=0.8):
    correlation = data.corr().abs()  # Compute absolute correlation matrix
    upper_triangle = correlation.where(np.triu(np.ones(correlation.shape), k=1).astype(bool))  # Get upper triangle of the correlation matrix
    columns_to_drop = [col for col in upper_triangle.columns if any(upper_triangle[col] > threshold)]  # Identify columns to drop

    # Print the pairs of features being dropped due to high correlation
    print("\nHighly correlated features (correlation > 0.8) that will be dropped:")
    for col in columns_to_drop:
        correlated_with = upper_triangle.index[upper_triangle[col] > threshold].tolist()
        for feature in correlated_with:
            print(f"{col} and {feature}: {correlation.loc[col, feature]:.2f}")

    reduced_features = data.drop(columns=columns_to_drop)  # Drop the identified features
    return reduced_features

# Apply the function to remove correlated features
reduced_corr_features = drop_high_correlation(features)

# Evaluate performance after removing correlated features
X_train, X_test, y_train, y_test = train_test_split(reduced_corr_features, target, test_size=0.2, random_state=42)

# Initialize and train the RandomForest model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions and calculate accuracy
y_pred_corr = rf_model.predict(X_test)
accuracy_after_correlation = accuracy_score(y_test, y_pred_corr)
print(f"\nAccuracy after dropping highly correlated features: {accuracy_after_correlation:.2f}")

def forward_selection(data, target):
    logistic_model = LogisticRegression(max_iter=1000)
    selector = SelectKBest(k='all').fit(data, target)
    feature_scores = selector.scores_
    ranked_features = np.argsort(feature_scores)[::-1]  # Rank features by score in descending order

    highest_accuracy = 0
    optimal_feature_count = 0

    for num_features in range(1, data.shape[1] + 1):
        selected_data = data.iloc[:, ranked_features[:num_features]]
        X_train, X_test, y_train, y_test = train_test_split(selected_data, target, test_size=0.2, random_state=42)
        logistic_model.fit(X_train, y_train)
        predictions = logistic_model.predict(X_test)
        current_accuracy = accuracy_score(y_test, predictions)

        if current_accuracy > highest_accuracy:
            highest_accuracy = current_accuracy
            optimal_feature_count = num_features

    return optimal_feature_count, highest_accuracy

# Run the forward feature selection process
optimal_features, accuracy_score_forward = forward_selection(features, target)
print(f"Optimal number of features using forward selection: {optimal_features}, Accuracy: {accuracy_score_forward:.2f}")

def backward_elimination(data, target):
    decision_tree = DecisionTreeClassifier(random_state=42)
    rfe_selector = RFE(estimator=decision_tree, n_features_to_select=1, step=1)
    rfe_selector.fit(data, target)
    feature_ranking = rfe_selector.ranking_
    top_features = np.argsort(feature_ranking)[:5]
    reduced_data = data.iloc[:, top_features]
    return reduced_data

# Apply backward feature elimination
reduced_backward_features = backward_elimination(features, target)

# Evaluate model performance after applying backward elimination
X_train, X_test, y_train, y_test = train_test_split(reduced_backward_features, target, test_size=0.2, random_state=42)
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)
predictions = dt_model.predict(X_test)
accuracy_after_backward = accuracy_score(y_test, predictions)

print(f"Accuracy after backward feature elimination: {accuracy_after_backward:.2f}")

def rf_feature_importance(data, target):
    rf_model = RandomForestClassifier(random_state=42)
    rf_model.fit(data, target)
    feature_importances = rf_model.feature_importances_
    top_indices = np.argsort(feature_importances)[::-1][:5]  # Indices of the top 5 most important features
    reduced_data = data.iloc[:, top_indices]
    return reduced_data, top_indices

# Apply the function to get the top 5 important features
reduced_rf_features, important_indices = rf_feature_importance(features, target)

# Evaluate model performance with the top 5 features
X_train, X_test, y_train, y_test = train_test_split(reduced_rf_features, target, test_size=0.2, random_state=42)
rf_model.fit(X_train, y_train)
predicted_values = rf_model.predict(X_test)
accuracy_rf_top5 = accuracy_score(y_test, predicted_values)

print(f"Accuracy with the top 5 important features: {accuracy_rf_top5:.2f}")