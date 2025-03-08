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
        # The expected class labels for the challenge
        self.label_names = [1, 2, 3, 4]
        self.rng = np.random.RandomState(self.random_state)

    def fit(self, X, y):
        # Store the classes from the training data
        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)
        return self

    def predict(self, X):
        """Return class labels.
        The RAMP framework may not use this method directly
        but we implement it correctly for completeness.
        """
        # Get the class with highest probability for each sample
        # +1 because classes are 1-indexed
        return np.argmax(self.predict_proba(X), axis=1) + 1

    def predict_proba(self, X):
        """Return probability estimates for each class.

        Returns a 2D array of shape (n_samples, 4) where each row sums to 1.
        """

        if self.classes_ is None:
            raise ValueError("Estimator not fitted yet.")

        n_samples = X.shape[0]

        # Always return a 2D array with exactly 4 columns (one per class)
        # The classes are [1, 2, 3, 4] but the columns are 0-indexed

        n_classes = 4
        probas = self.rng.rand(n_samples, n_classes)
        # Normalize to make each row sum to 1
        probas = probas / probas.sum(axis=1, keepdims=True)
        return probas


def get_estimator():
    """
    Returns a simple random predictor for testing GitHub Actions.
    This estimator makes completely random predictions and should not be used
    for actual model evaluation - it's only for testing workflow execution.
    """
    return RandomPredictor()
