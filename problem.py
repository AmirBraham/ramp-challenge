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


def load_data(path='.', dataset_file='train.csv', is_public=False):
    """
    Load a dataset from the specified CSV file.
    
    Parameters:
    -----------
    path: str
        Path to the data directory
    dataset_file: str
        Name of the CSV file to load
    is_public: bool
        Whether to load from the public directory
    
    Returns:
    --------
    X_df, y: tuple
        Features dataframe and target variable
    """
    data_path = Path(path) / "data"
    
    if is_public:
        data_path = data_path / "public"
    
    # Load the merged dataframe from CSV
    df = pd.read_csv(data_path / dataset_file)
    
    # Extract target variable
    y = df['grav']
    
    # Drop the target column from features
    X_df = df.drop(columns=['grav'])
    
    return X_df, y


def get_train_data(path='.'):
    """
    Get the training data
    
    Parameters:
    -----------
    path: str
        Path to the data directory
    
    Returns:
    --------
    X_df, y: tuple
        Features and target for training
    """
    # On the RAMP server, use the private training data
    # For local development, use the public training data
    try:
        return load_data(path, 'train.csv', is_public=False)
    except FileNotFoundError:
        print("Private training data not found, using public data...")
        return load_data(path, 'train.csv', is_public=True)


def get_test_data(path='.'):
    """
    Get the test data
    
    Parameters:
    -----------
    path: str
        Path to the data directory
    
    Returns:
    --------
    X_df, y: tuple
        Features and target for testing
    """
    # On the RAMP server, use the private test data
    # For local development, use the public test data
    try:
        return load_data(path, 'test.csv', is_public=False)
    except FileNotFoundError:
        print("Private test data not found, using public data...")
        return load_data(path, 'test.csv', is_public=True)
