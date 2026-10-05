# THIS IS MAIN LAB PYTHON FILE
import json

import pandas as pd
import numpy as np

from pathlib import Path
from sklearn import neighbors
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             mean_absolute_error, mean_squared_error, r2_score)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from copy import deepcopy

from config import CLASSIFIER, REGRESSOR, DATASETS, EXPERIMENT_CONFIG, PREPROCESS_NONE, PREPROCESS_STANDARD, PREPROCESS_MINMAX
from util import experiment_template, export_result

## CORE
def preprocess_data(
  X_train,
  X_test,
  preprocessing
):
  if preprocessing == PREPROCESS_NONE:
    return X_train, X_test

  if preprocessing == PREPROCESS_STANDARD:
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled

  if preprocessing == PREPROCESS_MINMAX:
    scaler = MinMaxScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled

  raise ValueError(f"Unsupported preprocessing: {preprocessing}")

def train_knn(model, X_train, y_train):
  model.fit(X_train, y_train)
  return model

def train_knn_classifier(X_train, y_train, metric, k_value):
  model_knn = neighbors.KNeighborsClassifier(n_neighbors=k_value, metric=metric)
  return train_knn(model_knn, X_train, y_train)

def train_knn_regressor(X_train, y_train, metric, k_value):
  model_knn = neighbors.KNeighborsRegressor(n_neighbors=k_value, metric=metric)
  return train_knn(model_knn, X_train, y_train)

def evaluate_knn_classifier(model_knn, X_test, y_test, labels):
  y_pred = model_knn.predict(X_test)
  model_accuracy = accuracy_score(y_test, y_pred)
  cm_result = confusion_matrix(y_test, y_pred, labels=labels)
  return model_accuracy, cm_result

def evaluate_knn_regressor(model_knn, X_test, y_test):
  y_pred = model_knn.predict(X_test)
  mae = mean_absolute_error(y_test, y_pred)
  mse = mean_squared_error(y_test, y_pred)
  rmse = np.sqrt(mse)
  r2 = r2_score(y_test, y_pred)
  return mae, mse, rmse, r2

def predict_first_knn_classifier(model_knn, X_test, y_test, n):
  X_predict = X_test[:n]
  y_actual = y_test[:n]

  y_pred = model_knn.predict(X_predict)

  predictions = []

  for i in range(n):
    actual = y_actual[i]
    predicted = y_pred[i]

    predictions.append({
      "index": i,
      "actual": actual.item(),
      "predicted": predicted.item(),
      "correct": bool(actual == predicted)
    })

  preview_accuracy = accuracy_score(y_actual, y_pred)
  return predictions, preview_accuracy

def predict_first_knn_regressor(model_knn, X_test, y_test, n):
  X_predict = X_test[:n]
  y_actual = y_test[:n]

  y_pred = model_knn.predict(X_predict)

  predictions = []

  for i in range(n):
    actual = y_actual[i]
    predicted = y_pred[i]

    predictions.append({
      "index": i,
      "actual": actual.item(),
      "predicted": predicted.item()
    })

  return predictions

## LOAD DATASET
def clean_dataset(df):
  df = df.dropna()
  return df

def load_dataset(dataset):
  config = DATASETS.get(dataset)

  if config is None:
    return False

  df = pd.read_csv(
    config["file"],
    sep=config.get("sep", ",")
  )
  df = clean_dataset(df)

  target = config["target"]

  if "features" in config:
    X = df[config["features"]].to_numpy()
  else:
    X = df.drop(columns=[target])
  y = df[target].to_numpy()

  task = config["task"]

  labels = (
    sorted(np.unique(y).tolist())
    if task == CLASSIFIER
    else []
  )

  return X, y, labels, dataset, task

## MAIN MODEL
def train_model_knn(dataset, directory_name):
  loaded = load_dataset(dataset)
  if loaded is False:
    return
  X, y, labels, dataset_name, task = loaded

  experiment_config = EXPERIMENT_CONFIG.get(dataset)
  if experiment_config is None:
    raise ValueError(
      f"No experiment configuration for dataset: {dataset}"
    )
  k_values = experiment_config["k_values"]
  splits = experiment_config["splits"]
  metrics = experiment_config["metrics"]
  preprocessing_list = experiment_config["preprocessing"]
  preview_config = experiment_config["evaluation"]["preview"]

  experiments = []
  experiment = deepcopy(experiment_template)
  experiment["metadata"]["dataset"]["name"] = dataset_name
  experiment["metadata"]["dataset"]["n_samples"] = X.shape[0]
  experiment["metadata"]["dataset"]["n_features"] = X.shape[1]
  experiment["metadata"]["dataset"]["n_classes"] = len(labels)
  experiment["metadata"]["dataset"]["classes"] = y.tolist()

  exp_id = 1
  for split in splits:
    for k_value in k_values:
      for metric in metrics:
        for preprocessing in preprocessing_list:
          experiment = deepcopy(experiment)
          experiment["id"] = f"EXP{exp_id:03d}"
          experiment["metadata"]["task"] = task

          experiment["metadata"]["dataset"]["name"] = dataset_name
          experiment["metadata"]["dataset"]["n_samples"] = X.shape[0]
          experiment["metadata"]["dataset"]["n_features"] = X.shape[1]

          experiment["metadata"]["split"]["train_ratio"] = (split.get("train_ratio"))

          experiment["metadata"]["split"]["test_ratio"] = (split.get("test_ratio"))

          experiment["metadata"]["split"]["random_state"] = (split.get("random_state"))

          experiment["metadata"]["split"]["label"] = (split.get("label"))

          experiment["metadata"]["model"]["k"] = k_value
          experiment["metadata"]["model"]["metric"] = (metric.get("value"))
          experiment["metadata"]["model"]["metric_label"] = (metric.get("label"))

          experiment["metadata"]["preprocessing"]["name"] = (preprocessing["value"])
          experiment["metadata"]["preprocessing"]["label"] = (preprocessing["label"])

          if task == CLASSIFIER:
            experiment["metadata"]["dataset"]["n_classes"] = len(labels)
            experiment["metadata"]["dataset"]["classes"] = labels

          X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=split.get("test_ratio"),
            random_state=split.get("random_state")
          )

          X_train, X_test = preprocess_data(
            X_train,
            X_test,
            preprocessing["value"]
          )

          if task == CLASSIFIER:
            model_knn = train_knn_classifier(
              X_train,
              y_train,
              metric.get("value"),
              k_value
            )

            model_accuracy, cm_result = evaluate_knn_classifier(
              model_knn,
              X_test,
              y_test,
              labels
            )

            experiment["result"]["accuracy"] = model_accuracy
            experiment["evaluation"]["confusion_matrix"] = (cm_result.tolist())

            if preview_config.get("enabled", True):
              preview_count = preview_config.get("count")
              predictions, preview_accuracy = predict_first_knn_classifier(
                  model_knn,
                  X_test,
                  y_test,
                  preview_count
                )

              experiment["evaluation"]["preview"]["count"] = preview_count
              experiment["evaluation"]["preview"]["accuracy"] = (preview_accuracy)
              experiment["evaluation"]["preview"]["predictions"] = (predictions)


          elif task == REGRESSOR:

            model_knn = train_knn_regressor(
              X_train,
              y_train,
              metric.get("value"),
              k_value
            )

            mae, mse, rmse, r2 = evaluate_knn_regressor(
              model_knn,
              X_test,
              y_test
            )

            experiment["result"]["mae"] = mae
            experiment["result"]["mse"] = mse
            experiment["result"]["rmse"] = rmse
            experiment["result"]["r2"] = r2


            if preview_config.get("enabled", True):
              preview_count = preview_config.get("count")
              predictions = predict_first_knn_regressor(
                  model_knn,
                  X_test,
                  y_test,
                  preview_count
                )

              experiment["evaluation"]["preview"]["count"] = preview_count
              experiment["evaluation"]["preview"]["predictions"] = (predictions)

          else:
            raise ValueError(f"Unsupported model task: {task}")

          experiments.append(experiment)
          exp_id += 1

  print(f"Total experiments: {len(experiments)}")
  print([experiment["id"] for experiment in experiments])

  export_dir = Path("./export") / directory_name
  export_dir.mkdir(parents=True, exist_ok=True)
  with open(
      export_dir / "experiments.json",
      "w",
      encoding="utf-8"
  ) as f:
    json.dump(
      experiments,
      f,
      ensure_ascii=False,
      indent=4
    )
  export_result(directory_name, task, experiment_config)

if __name__ == "__main__":
  print("Hello World")