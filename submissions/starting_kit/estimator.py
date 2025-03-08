import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin


class RandomPredictor(BaseEstimator, ClassifierMixin):
    """
    A dummy classifier that makes random predictions.
    This is used only to test that the GitHub Actions workflow is running
    correctly.
    """

    def __init__(self, random_state=42):
        self.random_state = random_state
        self.classes_ = None
        self.n_classes_ = None
        self.rng = np.random.RandomState(self.random_state)

    def fit(self, X, y):
        # Just store the classes
        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)
        return self

    def predict(self, X):
        # Generate random predictions
        if self.classes_ is None:
            raise ValueError("Estimator not fitted yet.")
        n_samples = X.shape[0]
        return self.rng.choice(self.classes_, size=n_samples)

    def predict_proba(self, X):
        # Generate random probabilities
        if self.classes_ is None:
            raise ValueError("Estimator not fitted yet.")
        n_samples = X.shape[0]
        # Generate random probabilities that sum to 1 for each sample
        probas = self.rng.rand(n_samples, self.n_classes_)
        probas = probas / probas.sum(axis=1, keepdims=True)
        return probas


def get_estimator():
    """
    Returns a simple random predictor for testing GitHub Actions.
    This estimator makes completely random predictions and should not be used
    for actual model evaluation - it's only for testing workflow execution.
    """
    return RandomPredictor()
