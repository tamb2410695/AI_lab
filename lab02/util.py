import json
import pandas as pd

from pathlib import Path
from config import CLASSIFIER, REGRESSOR
from export import export_classification_result, export_regression_result


def json_to_csv(json_file, csv_file):
  with open(json_file, "r", encoding="utf-8") as f:
    experiments = json.load(f)

  rows = []

  for experiment in experiments:
    metadata = experiment["metadata"]
    split = metadata["split"]
    model = metadata["model"]
    preprocessing = metadata["preprocessing"]
    result = experiment["result"]

    row = {
      "id": experiment["id"],
      "dataset": metadata["dataset"]["name"],

      "split": split["label"],
      "train_ratio": split["train_ratio"],
      "test_ratio": split["test_ratio"],
      "random_state": split["random_state"],

      "model": model["name"],
      "k": model["k"],
      "metric": model["metric"],
      "metric_label": model["metric_label"],

      "preprocessing": preprocessing["name"],
      "preprocessing_label": preprocessing["label"],

      "accuracy": result["accuracy"]
    }
    rows.append(row)

  df = pd.DataFrame(rows)
  df.to_csv(csv_file, index=False, encoding="utf-8-sig")

def export_preview(json_file, csv_file):
  with open(json_file, "r", encoding="utf-8") as f:
    experiments = json.load(f)

  rows = []

  for experiment in experiments:
    metadata = experiment["metadata"]
    preview = experiment["evaluation"]["preview"]

    if preview["count"] <= 0:
      continue

    predictions = preview["predictions"]

    for prediction in predictions:
      row = {
        "id": experiment["id"],

        "dataset": metadata["dataset"]["name"],

        "split": metadata["split"]["label"],

        "model": metadata["model"]["name"],
        "k": metadata["model"]["k"],
        "metric": metadata["model"]["metric"],
        "metric_label": metadata["model"]["metric_label"],

        "preprocessing": metadata["preprocessing"]["name"],
        "preprocessing_label": metadata["preprocessing"]["label"],

        "preview_count": preview["count"],
        "preview_accuracy": preview["accuracy"],

        "index": prediction["index"],
        "actual": prediction["actual"],
        "predicted": prediction["predicted"],
        "correct": prediction["correct"]
      }

      rows.append(row)

  df = pd.DataFrame(rows)

  df.to_csv(
    csv_file,
    index=False,
    encoding="utf-8-sig"
  )

experiment_template = {
  "id": None,

  "metadata": {
    "dataset": {
      "name": "Dataset",
      "n_samples": 0,
      "n_features": 0,
      "n_classes": 0,
      "classes": []
    },

    "split": {
      "method": "holdout",
      "train_ratio": None,
      "test_ratio": None,
      "label": None,
      "random_state": 42
    },

    "model": {
      "name": "KNN",
      "k": None,
      "metric": None,
      "metric_label": None
    },
    "preprocessing": {
      "name": None,
      "label": None
    }
  },

  "result": {
    "accuracy": None,
    "mae": None,
    "mse": None,
    "rmse": None,
    "r2": None
  },

  "evaluation": {
    "confusion_matrix": None,
    "preview": {
      "count": 0,
      "accuracy": None,
      "predictions": []
    }
  },

}

def json_to_dataframe(experiments):
  rows = []

  for experiment in experiments:
    metadata = experiment["metadata"]
    split = metadata["split"]
    model = metadata["model"]
    preprocessing = metadata["preprocessing"]
    result = experiment["result"]

    rows.append({
      "id": experiment["id"],
      "dataset": metadata["dataset"]["name"],

      "split": split["label"],
      "train_ratio": split["train_ratio"],
      "test_ratio": split["test_ratio"],
      "random_state": split["random_state"],

      "model": model["name"],
      "k": model["k"],
      "metric": model["metric"],
      "metric_label": model["metric_label"],

      "preprocessing": preprocessing["name"],
      "preprocessing_label": preprocessing["label"],

      "accuracy": result["accuracy"],
      "mae": result["mae"],
      "mse": result["mse"],
      "rmse": result["rmse"],
      "r2": result["r2"]
    })

  return pd.DataFrame(rows)


def export_result(directory_name, task, experiment_config):
  export_dir = Path("./export") / directory_name

  input_file = export_dir / "experiments.json"
  output_file = export_dir / "experiments.csv"
  output_preview_file = export_dir / "preview_predictions.csv"

  with open(input_file, "r", encoding="utf-8") as f:
    experiments = json.load(f)

  k_values = experiment_config["k_values"]
  splits = experiment_config["splits"]
  metrics = experiment_config["metrics"]
  preprocessing = experiment_config["preprocessing"]
  preview_config = experiment_config["evaluation"]["preview"]

  # JSON → CSV
  json_to_csv(input_file, output_file)
  if preview_config:
    export_preview(input_file, output_preview_file)

  df = json_to_dataframe(experiments)

  if task == CLASSIFIER:
    export_classification_result(
      directory_name,
      df,
      k_values,
      splits,
      metrics,
      preprocessing
    )

  elif task == REGRESSOR:
    export_regression_result(
      directory_name,
      df,
      k_values,
      splits,
      metrics,
      preprocessing
    )

  else:
    raise ValueError(f"Unsupported task: {task}")
