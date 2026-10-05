# DATASET
"""
  You can name your dataset here and use this to manage it easier
"""
DATASET_IRIS = "Iris"
DATASET_WINE_RED = "Wine Red"
DATASET_WINE_WHITE = "Wine White"
DATASET_HOUSING = "Housing"

# MODEL
KNN = "knn"

# TASK
CLASSIFIER = "classifier"
REGRESSOR = "regressor"

# PREPROCESS
PREPROCESS_NONE = "none"
PREPROCESS_STANDARD = "standard"
PREPROCESS_MINMAX = "minmax"

"""
  Here is where you set dataset config
  You should do it like bellow
"""
DATASETS = {
  DATASET_IRIS: {
    "file": "./dataset/iris_data.csv",
    "sep": ",",
    "target": "nhan",
    "task": CLASSIFIER,
    "features": [
      "sepalLength",
      "sepalWidth",
      "petalLength",
      "petalWidth"
    ]
  },

  DATASET_WINE_RED: {
    "file": "./dataset/winequality-red.csv",
    "sep": ";",
    "target": "quality",
    "task": CLASSIFIER,
    "features": [
      "fixed acidity",
      "volatile acidity",
      "citric acid",
      "residual sugar",
      "chlorides",
      "free sulfur dioxide",
      "total sulfur dioxide",
      "density",
      "pH",
      "sulphates",
      "alcohol"
    ]
  },
  DATASET_WINE_WHITE: {
    "file": "./dataset/winequality-white.csv",
    "sep": ";",
    "target": "quality",
    "task": CLASSIFIER,
    "features": [
      "fixed acidity",
      "volatile acidity",
      "citric acid",
      "residual sugar",
      "chlorides",
      "free sulfur dioxide",
      "total sulfur dioxide",
      "density",
      "pH",
      "sulphates",
      "alcohol"
    ]
  },

  DATASET_HOUSING: {
    "file": "./dataset/HousingData.csv",
    "target": "MEDV",
    "task": REGRESSOR,
    "features": [
      "CRIM",
      "ZN",
      "INDUS",
      "CHAS",
      "NOX",
      "RM",
      "AGE",
      "DIS",
      "RAD",
      "TAX",
      "PTRATIO",
      "B",
      "LSTAT"
    ]
  }
}

"""
  Here is where you set dataset config
  You should do it like bellow
"""
# EXPERIMENT CONFIGURATION
EXPERIMENT_CONFIG = {
  DATASET_IRIS: {
    "k_values": [1, 2, 4, 6, 8, 10],

    "splits": [
      {
        "train_ratio": 2/3,
        "test_ratio": 1/3,
        "label": "2/3 - 1/3",
        "file_label": "2_3_1_3",
        "random_state": 42
      },
      {
        "train_ratio": 0.8,
        "test_ratio": 0.2,
        "label": "80% - 20%",
        "file_label": "80_20",
        "random_state": 42
      },
    ],

    "metrics": [
      {
        "value": "manhattan",
        "label": "Manhattan"
      },
      {
        "value": "euclidean",
        "label": "Euclidean"
      }
    ],

    "preprocessing": [
      {
        "value": PREPROCESS_NONE,
        "label": "Original"
      }
    ],

    "evaluation": {
      "preview": {
          "enabled": False,
          "count": 0,
      }
    }
  },

  DATASET_WINE_RED: {
    "k_values": [9],

    "splits": [
      {
        "train_ratio": 4/5,
        "test_ratio": 1/5,

        "label": "4/5 - 1/5",
        "file_label": "4_5_1_5",

        "random_state": 42
      }
    ],

    "metrics": [
      {
        "value": "euclidean",
        "label": "Euclidean"
      }
    ],

    "preprocessing": [
      {
        "value": PREPROCESS_NONE,
        "label": "Before Scaling"
      },
      {
        "value": PREPROCESS_MINMAX,
        "label": "After Scaling"
      }
    ],

    "evaluation": {
      "preview": {
        "enabled": True,
        "count": 7,
      }
    }
  },

  DATASET_WINE_WHITE: {
    "k_values": [7],

    "splits": [
      {
        "train_ratio": 0.8,
        "test_ratio": 0.2,
        "label": "80% - 20%",
        "file_label": "80_20",
        "random_state": 42
      }
    ],

    "metrics": [
      {
        "value": "euclidean",
        "label": "Euclidean"
      }
    ],

    "preprocessing": [
      {
        "value": PREPROCESS_NONE,
        "label": "Before Scaling"
      },
      {
        "value": PREPROCESS_MINMAX,
        "label": "After Scaling"
      }
    ],

    "evaluation": {
      "preview": {
          "enabled": True,
          "count": 8,
      }
    }
  },

  DATASET_HOUSING: {
    "k_values": [1, 3, 5, 7, 9],

    "splits": [
      {
        "train_ratio": 0.8,
        "test_ratio": 0.2,
        "label": "80% - 20%",
        "file_label": "80_20",
        "random_state": 42
      }
    ],

    "metrics": [
      {
        "value": "euclidean",
        "label": "Euclidean"
      },
      {
        "value": "manhattan",
        "label": "Manhattan"
      }
    ],

    "preprocessing": [
      {
        "value": PREPROCESS_NONE,
        "label": "Before Scaling"
      },
      {
        "value": PREPROCESS_MINMAX,
        "label": "After Scaling"
      }
    ],

    "evaluation": {
      "preview": {
          "enabled": False,
          "count": 0,
      }
    }
  }
}
