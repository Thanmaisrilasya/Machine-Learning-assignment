# -*- coding: utf-8 -*-
"""K NN(iris data set).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1chUWUQujXSrV8mjI7MxLeRBaRPD5aKD4
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('iris.csv').values
np.random.shuffle(data)

label_mapping = {label: idx for idx, label in enumerate(np.unique(data[:, -1]))}
y = np.array([label_mapping[label] for label in data[:, -1]])
X = data[:, :-1]

split_index = int(0.75 * len(data))
X_train, X_test = X[:split_index], X[split_index:]
y_train, y_test = y[:split_index], y[split_index:]

def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))

def manual_knn(X_train, y_train, X_test, k):
    predictions = []
    for test_point in X_test:
        distances = []
        for i in range(len(X_train)):
            dist = euclidean_distance(test_point, X_train[i])
            distances.append((dist, y_train[i]))

        distances.sort(key=lambda x: x[0])
        k_nearest_neighbors = distances[:k]
        k_nearest_labels = [label for _, label in k_nearest_neighbors]

        label_count = {}
        for label in k_nearest_labels:
            if label in label_count:
                label_count[label] += 1
            else:
                label_count[label] = 1

        most_common_label = max(label_count, key=label_count.get)
        predictions.append(most_common_label)

    return np.array(predictions)

def accuracy(y_true, y_pred):
    correct = 0
    for i in range(len(y_true)):
        if y_true[i] == y_pred[i]:
            correct += 1
    return correct / len(y_true)

def confusion_matrix(y_true, y_pred):
    unique_labels = np.unique(y_true)
    matrix = np.zeros((len(unique_labels), len(unique_labels)), dtype=int)

    for i in range(len(y_true)):
        true_label = y_true[i]
        predicted_label = y_pred[i]
        matrix[true_label, predicted_label] += 1

    return matrix

k = 5
y_pred = manual_knn(X_train, y_train, X_test, k)

acc = accuracy(y_test, y_pred)
print(f'Accuracy for k={k}: {acc:.4f}')

conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_matrix)

k_values = range(1, 11)
accuracies = []

for k in k_values:
    y_pred = manual_knn(X_train, y_train, X_test, k)
    acc = accuracy(y_test, y_pred)
    accuracies.append(acc)

plt.plot(k_values, accuracies, marker='o')
plt.xlabel('K')
plt.ylabel('Accuracy (decimal)')
plt.title('K vs Accuracy')
plt.grid(True)
plt.show()

best_k = k_values[np.argmax(accuracies)]
print(f'Best K: {best_k} with accuracy {max(accuracies):.4f}')