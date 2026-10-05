from pandas import read_csv
import numpy as np

from sklearn import neighbors, datasets
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def iris_pandas():
  iris = read_csv('dataset/iris_data.csv', delimiter=',', index_col=0)

  iris_X = iris.iloc[:, :-1]
  iris_y = iris.iloc[:, -1]

  iris_y = iris_y.map({'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2})

  print("Number of classes:", len(np.unique(iris_y)))
  print("Number of data:", len(iris_y))
  print()

  for i in range(3):
    print(f"Sample data from class {i}:")
    print(iris_X[iris_y == i].head())
    print()

def iris_sklearn():
  iris = datasets.load_iris()

  iris_X = iris.data
  iris_y = iris.target

  print("Number of classes:", len(np.unique(iris_y)))
  print("Number of data:", len(iris_y))
  print()

  x0 = iris_X[iris_y == 0, :]
  print("Sample data from class 0:")
  print(x0[:5, :])
  x1 = iris_X[iris_y == 1, :]
  print("Sample data from class 1:")
  print(x1[:5, :])
  x2 = iris_X[iris_y == 2, :]
  print("Sample data from class 2:")
  print(x2[:5, :])

def calculate_accuracy_per_class(conf_matrix):
  accuracies = []
  for i in range(len(conf_matrix)):
    correct_predictions = conf_matrix[i, i]
    total_predictions = np.sum(conf_matrix[i, :])
    accuracy = correct_predictions / total_predictions if total_predictions != 0 else 0
    accuracies.append(accuracy)
  return accuracies

def model_knn_classifier(cm_type: int):
  iris = datasets.load_iris()

  iris_X = iris.data
  iris_y = iris.target

  X_train, X_test, y_train, y_test = train_test_split(iris_X, iris_y, test_size=50)

  print("Training size: %d" % len(y_train))
  print("Test size    : %d" % len(y_test))
  print(y_test)

  model_knn = neighbors.KNeighborsClassifier(n_neighbors=3, p=2)
  model_knn.fit(X_train, y_train)

  y_pred = model_knn.predict(X_test)

  print("Print result for 20 test data points")
  print("Predicted labels :", y_pred[0:20])
  print("Gournd truth     :", y_test[0:20])

  print("Accuracy of KNN: %.2f %%" % (100 * accuracy_score(y_test, y_pred)))

  if cm_type == 1:
    print("Confusion matrix - Sklearn:")
    cm = confusion_matrix(y_test, y_pred, labels=[2, 0, 1])
    print(cm)

  if cm_type == 2:
    print("Confusion matrix - Pandas + Matplotlib + Seaborn:")
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1, 2])
    cm_df = pd.DataFrame(cm, index=['SETOSA', 'VERSICOLR', 'VIRGINICA'],
                         columns=['SETOSA', 'VERSICOLR', 'VIRGINICA'])

    plt.figure(figsize=(5, 4))
    sns.heatmap(cm_df, annot=True)
    plt.title("Confusion Matrix")
    plt.ylabel("Actual Values")
    plt.xlabel("Presdicted Values")
    plt.show()

    accuracies = calculate_accuracy_per_class(cm)
    for i, accuracy in enumerate(accuracies):
      print(f"Accuracy of class {i} ({cm_df.index[i]}): {accuracy: .2f}")
