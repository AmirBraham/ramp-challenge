import rampwf as rw
from pathlib import Path
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import accuracy_score
import numpy as np

problem_title = 'Road Accident Severity Prediction'

_prediction_label_names = [1, 2, 3, 4]

Predictions = rw.prediction_types.make_multiclass(
    label_names=_prediction_label_names
)

workflow = rw.workflows.Estimator()

score_types = [
    rw.score_types.Accuracy(name='accuracy', precision=4),
]


def get_cv(X, y):
    cv = StratifiedShuffleSplit(n_splits=8, test_size=0.2, random_state=57)
    return cv.split(X, y)


def load_data(path='.', file='X_train.csv'):
    path = Path(path) / "data"
    X_df = pd.read_csv(path / file)

    y = X_df['target']
    X_df = X_df.drop(columns=['target'])

    return X_df, y


# READ DATA
def get_train_data(path='.'):
    file = 'X_train.csv'
    return load_data(path, file)


def get_test_data(path='.'):
    file = 'X_test.csv'
    return load_data(path, file)
