from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
import pandas as pd
import numpy as np


def get_estimator():
    """
    Returns a pipeline for classifying road accident severity,
    handling mixed data types efficiently.
    """
    # Dynamic preprocessing pipeline
    class PreprocessingPipeline:
        def __init__(self):
            self.preprocessor = None
            self.fitted = False
            self.column_dtypes = None
        
        def fit(self, X, y=None):
            # Convert to DataFrame if needed
            if isinstance(X, np.ndarray):
                X = pd.DataFrame(X)
            
            # Store initial column dtypes for transform step
            self.column_dtypes = X.dtypes.to_dict()
            
            # Identify and fix mixed type columns
            mixed_cols = []
            for col in X.columns:
                # Check if column has mixed types
                try:
                    unique_types = X[col].apply(type).unique()
                    if len(unique_types) > 1:
                        # Convert mixed type columns to string
                        X[col] = X[col].astype(str)
                        mixed_cols.append(col)
                except (TypeError, ValueError):
                    # If error occurs during type checking, convert to string
                    X[col] = X[col].astype(str)
                    mixed_cols.append(col)
            
            # Now detect column types after fixing mixed columns
            numerical_cols = X.select_dtypes(
                include=['float64', 'int64']).columns.tolist()
            categorical_cols = X.select_dtypes(
                include=['object', 'category', 'string']).columns.tolist()
            
            # Build the column transformer
            transformers = []
            
            # Only add numerical pipeline if we have numerical columns
            if numerical_cols:
                transformers.append(('num', make_pipeline(
                    SimpleImputer(strategy='median'),
                    StandardScaler()
                ), numerical_cols))
            
            # Only add categorical pipeline if we have categorical columns
            if categorical_cols:
                # Use sparse output for memory efficiency
                transformers.append(('cat', make_pipeline(
                    SimpleImputer(strategy='constant', fill_value='missing'),
                    OneHotEncoder(handle_unknown='ignore', sparse_output=True,
                                  max_categories=20)
                ), categorical_cols))
            
            self.preprocessor = ColumnTransformer(
                transformers=transformers,
                remainder='drop',  # Drop any columns not explicitly handled
                sparse_threshold=0.8  # Use sparse when beneficial
            )
            
            # Fit the preprocessor
            self.preprocessor.fit(X, y)
            self.fitted = True
            return self
        
        def transform(self, X):
            if not self.fitted:
                raise ValueError("Pipeline not fitted yet")
            
            # Convert to DataFrame if needed
            if isinstance(X, np.ndarray):
                X = pd.DataFrame(X)
            
            # Apply the same type conversions as in fit
            for col in X.columns:
                if col in self.column_dtypes:
                    # If it was a mixed column, convert to string
                    try:
                        unique_types = X[col].apply(type).unique()
                        if len(unique_types) > 1:
                            X[col] = X[col].astype(str)
                    except (TypeError, ValueError):
                        X[col] = X[col].astype(str)
            
            return self.preprocessor.transform(X)
        
        def fit_transform(self, X, y=None):
            return self.fit(X, y).transform(X)
    
    # Set up the classifier with proper parameters
    rf_classifier = RandomForestClassifier(
        n_estimators=50, 
        random_state=42,
        max_features='sqrt', 
        max_depth=10,
        class_weight='balanced'
    )
    
    # Main pipeline: memory-efficient with feature selection
    return make_pipeline(
        PreprocessingPipeline(),
        # Add feature selection to reduce dimensionality
        SelectFromModel(
            RandomForestClassifier(n_estimators=10, max_depth=5, 
                                   random_state=42)
        ),
        # Final classifier with reduced complexity
        rf_classifier
    )
