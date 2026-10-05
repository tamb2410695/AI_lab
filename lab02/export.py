import matplotlib.pyplot as plt

## Helper export
def get_preprocessing_values(preprocessing):
  return [item["value"] for item in preprocessing]

def get_preprocessing_label(preprocessing, value):
  for item in preprocessing:
    if item["value"] == value:
      return item["label"]

  return value

def export_classification_by_k(
  directory_name,
  df,
  k_values,
  splits,
  metrics,
  preprocessing
):
  for split in splits:

    split_label = split["label"]
    file_label = split["file_label"]

    df_split = df[
      df["split"] == split_label
    ]

    for preprocess in preprocessing:

      preprocess_value = preprocess["value"]
      preprocess_label = preprocess["label"]

      df_preprocess = df_split[
        df_split["preprocessing"] == preprocess_value
      ]

      plt.figure(figsize=(9, 6))

      for metric in metrics:

        metric_value = metric["value"]
        metric_label = metric["label"]

        df_metric = (
          df_preprocess[
            df_preprocess["metric"] == metric_value
          ]
          .sort_values("k")
        )

        plt.plot(
          df_metric["k"],
          df_metric["accuracy"],
          marker="o",
          markersize=6,
          linewidth=2,
          label=metric_label
        )

      plt.xlabel(
        "Number of Neighbors (k)",
        fontsize=11
      )

      plt.ylabel(
        "Accuracy",
        fontsize=11
      )

      plt.title(
        f"KNN Classification - "
        f"{split_label} - "
        f"{preprocess_label}",
        fontsize=14,
        fontweight="bold"
      )

      plt.xticks(k_values)

      plt.legend(
        title="Distance Metric",
        fontsize=10
      )

      plt.grid(
        True,
        linestyle="--",
        alpha=0.4
      )

      plt.tight_layout()

      plt.savefig(
        f"./export/{directory_name}/"
        f"KNN_{file_label}_"
        f"{preprocess_value}_by_k.png",
        dpi=300,
        bbox_inches="tight"
      )

      plt.close()

def export_classification_by_preprocessing(
  directory_name,
  df,
  k_values,
  splits,
  metrics,
  preprocessing
):
  preprocessing_values = [
    item["value"]
    for item in preprocessing
  ]

  preprocessing_labels = [
    item["label"]
    for item in preprocessing
  ]

  for split in splits:

    split_label = split["label"]
    file_label = split["file_label"]

    df_split = df[
      df["split"] == split_label
    ]

    for metric in metrics:

      metric_value = metric["value"]
      metric_label = metric["label"]

      plt.figure(figsize=(9, 6))

      for k_value in k_values:

        values = []

        for preprocessing_value in preprocessing_values:

          df_result = df_split[
            (df_split["metric"] == metric_value) &
            (df_split["k"] == k_value) &
            (
              df_split["preprocessing"]
              == preprocessing_value
            )
          ]

          if df_result.empty:
            values.append(None)
          else:
            values.append(
              df_result["accuracy"].iloc[0]
            )

        plt.plot(
          preprocessing_labels,
          values,
          marker="o",
          markersize=6,
          linewidth=2,
          label=f"k={k_value}"
        )

      plt.xlabel(
        "Preprocessing",
        fontsize=11
      )

      plt.ylabel(
        "Accuracy",
        fontsize=11
      )

      plt.title(
        f"KNN Classification - "
        f"Preprocessing Comparison - "
        f"{split_label} - "
        f"{metric_label}",
        fontsize=14,
        fontweight="bold"
      )

      plt.legend(
        title="Number of Neighbors",
        fontsize=10
      )

      plt.grid(
        True,
        linestyle="--",
        alpha=0.4
      )

      plt.tight_layout()

      plt.savefig(
        f"./export/{directory_name}/"
        f"KNN_{file_label}_"
        f"{metric_value}_preprocessing.png",
        dpi=300,
        bbox_inches="tight"
      )

      plt.close()

def export_regression_by_k(
  directory_name,
  df,
  k_values,
  splits,
  metrics,
  preprocessing
):
  regression_metrics = [
    ("mae", "MAE"),
    ("mse", "MSE"),
    ("rmse", "RMSE"),
    ("r2", "R²")
  ]

  for split in splits:

    split_label = split["label"]
    file_label = split["file_label"]

    df_split = df[
      df["split"] == split_label
    ]

    for preprocess in preprocessing:

      preprocess_value = preprocess["value"]
      preprocess_label = preprocess["label"]

      df_preprocess = df_split[
        df_split["preprocessing"] == preprocess_value
      ]

      for result_column, result_label in regression_metrics:

        plt.figure(figsize=(9, 6))

        for metric in metrics:

          metric_value = metric["value"]
          metric_label = metric["label"]

          df_metric = (
            df_preprocess[
              df_preprocess["metric"] == metric_value
            ]
            .sort_values("k")
          )

          plt.plot(
            df_metric["k"],
            df_metric[result_column],
            marker="o",
            markersize=6,
            linewidth=2,
            label=metric_label
          )

        plt.xlabel(
          "Number of Neighbors (k)",
          fontsize=11
        )

        plt.ylabel(
          result_label,
          fontsize=11
        )

        plt.title(
          f"KNN Regression Performance - "
          f"{result_label} - "
          f"{split_label} - "
          f"{preprocess_label}",
          fontsize=14,
          fontweight="bold"
        )

        plt.xticks(k_values)

        plt.legend(
          title="Distance Metric",
          fontsize=10
        )

        plt.grid(
          True,
          linestyle="--",
          alpha=0.4
        )

        plt.tight_layout()

        plt.savefig(
          f"./export/{directory_name}/"
          f"KNN_{file_label}_"
          f"{preprocess_value}_"
          f"{result_column}_by_k.png",
          dpi=300,
          bbox_inches="tight"
        )

        plt.close()

def export_regression_by_preprocessing(
  directory_name,
  df,
  k_values,
  splits,
  metrics,
  preprocessing
):
  regression_metrics = [
    ("mae", "MAE"),
    ("mse", "MSE"),
    ("rmse", "RMSE"),
    ("r2", "R²")
  ]

  preprocessing_values = [
    item["value"]
    for item in preprocessing
  ]

  preprocessing_labels = [
    item["label"]
    for item in preprocessing
  ]

  for split in splits:

    split_label = split["label"]
    file_label = split["file_label"]

    df_split = df[
      df["split"] == split_label
    ]

    for metric in metrics:

      metric_value = metric["value"]
      metric_label = metric["label"]

      for result_column, result_label in regression_metrics:

        plt.figure(figsize=(9, 6))

        for k_value in k_values:

          values = []

          for preprocessing_value in preprocessing_values:

            df_result = df_split[
              (df_split["metric"] == metric_value) &
              (df_split["k"] == k_value) &
              (
                df_split["preprocessing"]
                == preprocessing_value
              )
            ]

            if df_result.empty:
              values.append(None)
            else:
              values.append(
                df_result[result_column].iloc[0]
              )

          plt.plot(
            preprocessing_labels,
            values,
            marker="o",
            markersize=6,
            linewidth=2,
            label=f"k={k_value}"
          )

        plt.xlabel(
          "Preprocessing",
          fontsize=11
        )

        plt.ylabel(
          result_label,
          fontsize=11
        )

        plt.title(
          f"KNN Regression - "
          f"{result_label} - "
          f"Preprocessing Comparison - "
          f"{split_label} - "
          f"{metric_label}",
          fontsize=14,
          fontweight="bold"
        )

        plt.legend(
          title="Number of Neighbors",
          fontsize=10
        )

        plt.grid(
          True,
          linestyle="--",
          alpha=0.4
        )

        plt.tight_layout()

        plt.savefig(
          f"./export/{directory_name}/"
          f"KNN_{file_label}_"
          f"{metric_value}_"
          f"{result_column}_"
          f"preprocessing.png",
          dpi=300,
          bbox_inches="tight"
        )

        plt.close()

def export_classification_result(
  directory_name,
  df,
  k_values,
  splits,
  metrics,
  preprocessing
):

  if len(k_values) > 1:
    export_classification_by_k(
      directory_name,
      df,
      k_values,
      splits,
      metrics,
      preprocessing
    )

  if len(preprocessing) > 1:
    export_classification_by_preprocessing(
      directory_name,
      df,
      k_values,
      splits,
      metrics,
      preprocessing
    )

def export_regression_result(
  directory_name,
  df,
  k_values,
  splits,
  metrics,
  preprocessing
):

  if len(k_values) > 1:

    export_regression_by_k(
      directory_name,
      df,
      k_values,
      splits,
      metrics,
      preprocessing
    )

  if len(preprocessing) > 1:

    export_regression_by_preprocessing(
      directory_name,
      df,
      k_values,
      splits,
      metrics,
      preprocessing
    )