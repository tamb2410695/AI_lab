"""
  README
  You must set your dataset directory and config in config.py before run main.py
"""

from config import DATASET_IRIS, DATASET_WINE_RED, DATASET_HOUSING, DATASET_WINE_WHITE
from knn_model import train_model_knn

# Question 1
def question01():
  train_model_knn(DATASET_IRIS, "iris")

# Lesson 1
def lesson01():
  train_model_knn(DATASET_HOUSING, "housing")

def lesson02():
  train_model_knn(DATASET_WINE_RED, "wine_red")

def lesson03():
  train_model_knn(DATASET_WINE_WHITE, "wine_white")

if __name__ == "__main__":
  print("Hello World")
  lesson03()