"""Utility functions for ML project generator."""

def get_docstring_template(class_name: str, template_type: str) -> str:
    """Generate a docstring template based on class name and template type."""
    docstrings = {
        "model": f'''"""
{class_name}

A machine learning model implementation.

Attributes:
    model: The underlying ML model instance.

Methods:
    fit(X, y): Train the model on the given data.
    predict(X): Make predictions on new data.
    evaluate(X, y): Evaluate model performance.
"""''',
        "preprocessing": '''"""
Data preprocessing utilities.

This module contains functions for data preprocessing and feature engineering.

Functions:
    preprocess_data(data): Preprocess the input data.
    feature_engineering(data): Create new features from existing data.
    handle_missing_values(data): Handle missing values in the dataset.
"""''',
        "training": '''"""
Model training utilities.

This module contains functions for model training and evaluation.

Functions:
    train_model(model, X, y): Train the model on the given data.
    evaluate_model(model, X, y): Evaluate model performance.
    save_model(model, path): Save the trained model.
    load_model(path): Load a saved model.
"""''',
        "visualization": '''"""
Data visualization utilities.

This module contains functions for data and model visualization.

Functions:
    plot_feature_importance(model, feature_names): Plot feature importance.
    plot_learning_curve(model, X, y): Plot learning curve.
    plot_confusion_matrix(y_true, y_pred): Plot confusion matrix.
"""'''
    }
    return docstrings.get(template_type, "")

def get_example_code(template_type: str) -> str:
    """Generate example code based on template type."""
    examples = {
        "model": '''# Example usage:
model = Model()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
''',
        "preprocessing": '''# Example usage:
processed_data = preprocess_data(raw_data)
features = feature_engineering(processed_data)
''',
        "training": '''# Example usage:
model = train_model(X_train, y_train)
metrics = evaluate_model(model, X_test, y_test)
''',
        "visualization": '''# Example usage:
plot_feature_importance(model, feature_names)
plot_learning_curve(model, X, y)
'''
    }
    return examples.get(template_type, "")

def get_config_template() -> str:
    """Generate a configuration template."""
    return '''"""
Configuration settings for the ML project.

This module contains all configuration parameters for the project.

Attributes:
    DATA_PATH: Path to the data directory
    MODEL_PATH: Path to save trained models
    LOG_PATH: Path to save logs
    BATCH_SIZE: Batch size for training
    LEARNING_RATE: Learning rate for optimization
    NUM_EPOCHS: Number of training epochs
"""

# Data paths
DATA_PATH = "data"
RAW_DATA_PATH = f"{DATA_PATH}/raw"
PROCESSED_DATA_PATH = f"{DATA_PATH}/processed"

# Model parameters
MODEL_PATH = "models"
LOG_PATH = f"{MODEL_PATH}/logs"
SAVE_MODEL_PATH = f"{MODEL_PATH}/saved"

# Training parameters
BATCH_SIZE = 32
LEARNING_RATE = 0.001
NUM_EPOCHS = 100

# Feature parameters
FEATURE_COLUMNS = [
    "feature1",
    "feature2",
    "feature3"
]

TARGET_COLUMN = "target"

# Model hyperparameters
MODEL_PARAMS = {
    "hidden_size": 64,
    "num_layers": 2,
    "dropout": 0.1
}
'''

def get_test_template(class_name: str) -> str:
    """Generate a test template."""
    return f'''"""
Tests for {class_name}.

This module contains unit tests for the {class_name} class.
"""

import pytest
from src.models.model import {class_name}

def test_{class_name.lower()}_initialization():
    """Test model initialization."""
    model = {class_name}()
    assert model is not None

def test_{class_name.lower()}_training():
    """Test model training."""
    model = {class_name}()
    # Add your test code here
    pass

def test_{class_name.lower()}_prediction():
    """Test model prediction."""
    model = {class_name}()
    # Add your test code here
    pass
'''
