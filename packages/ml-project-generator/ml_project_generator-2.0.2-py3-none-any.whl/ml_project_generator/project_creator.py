import os
import sys
import subprocess
import logging
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional
from .utils import (
    get_docstring_template,
    get_example_code,
    get_config_template,
    get_test_template
)

class ProjectTemplate(Enum):
    BASIC = "basic"
    DEEP_LEARNING = "deep_learning"
    NLP = "nlp"
    COMPUTER_VISION = "computer_vision"

def get_template_dependencies(template: ProjectTemplate) -> list:
    """Get dependencies based on project template."""
    base_deps = ["numpy>=1.21", "pandas>=1.3", "scikit-learn>=1.0"]
    
    template_deps = {
        ProjectTemplate.BASIC: [],
        ProjectTemplate.DEEP_LEARNING: ["torch>=2.0", "torchvision>=0.15"],
        ProjectTemplate.NLP: ["transformers>=4.30", "torch>=2.0", "nltk>=3.8"],
        ProjectTemplate.COMPUTER_VISION: ["torch>=2.0", "torchvision>=0.15", "opencv-python>=4.8"]
    }
    
    return base_deps + template_deps.get(template, [])

def get_template_files(project_name: str, template: ProjectTemplate) -> dict:
    """Get template-specific files based on project type."""
    base_files = {
        os.path.join(project_name, "src", "__init__.py"): "# src package initializer\n",
        os.path.join(project_name, "src", "main.py"): """# Main pipeline execution script
import logging
from pathlib import Path
import yaml

def load_config():
    config_path = Path("config/config.yaml")
    with open(config_path) as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    logging.info(f"Starting {config['project_name']} pipeline...")
    # Add your pipeline steps here

if __name__ == "__main__":
    main()
""",
    }

    # Notebook templates for each project type
    notebook_templates = {
        ProjectTemplate.BASIC: {
            os.path.join(project_name, "notebooks", "01_data_exploration.ipynb"): """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Data Exploration and Analysis\\n\\nThis notebook demonstrates basic data exploration techniques using pandas and matplotlib."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "import pandas as pd\\nimport matplotlib.pyplot as plt\\nimport seaborn as sns\\n\\n# Load your data\\ndata = pd.read_csv('../data/raw/your_data.csv')\\n\\n# Display basic information\\nprint('Dataset Info:')\\ndata.info()\\n\\n# Display first few rows\\nprint('\\nFirst few rows:')\\ndata.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Basic Statistics"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Display basic statistics\\ndata.describe()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}""",
            os.path.join(project_name, "notebooks", "02_model_training.ipynb"): """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Model Training and Evaluation\\n\\nThis notebook shows how to train and evaluate a basic ML model."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "from sklearn.model_selection import train_test_split\\nfrom sklearn.metrics import accuracy_score, classification_report\\nfrom src.models.model import Model\\n\\n# Load and preprocess data\\nX = data.drop('target', axis=1)\\ny = data['target']\\n\\n# Split data\\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\\n\\n# Train model\\nmodel = Model()\\nmodel.fit(X_train, y_train)\\n\\n# Make predictions\\ny_pred = model.predict(X_test)\\n\\n# Evaluate\\nprint('Accuracy:', accuracy_score(y_test, y_pred))\\nprint('\\nClassification Report:')\\nprint(classification_report(y_test, y_pred))"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}"""
        },
        ProjectTemplate.DEEP_LEARNING: {
            os.path.join(project_name, "notebooks", "01_data_preparation.ipynb"): """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Deep Learning Data Preparation\\n\\nThis notebook demonstrates how to prepare data for deep learning models."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "import torch\\nfrom torch.utils.data import Dataset, DataLoader\\n\\n# Define custom dataset\\nclass CustomDataset(Dataset):\\n    def __init__(self, X, y):\\n        self.X = torch.FloatTensor(X)\\n        self.y = torch.FloatTensor(y)\\n    \\n    def __len__(self):\\n        return len(self.y)\\n    \\n    def __getitem__(self, idx):\\n        return self.X[idx], self.y[idx]\\n\\n# Create data loaders\\ntrain_dataset = CustomDataset(X_train, y_train)\\ntrain_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}""",
            os.path.join(project_name, "notebooks", "02_model_training.ipynb"): """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Deep Learning Model Training\\n\\nThis notebook demonstrates how to train a deep learning model using PyTorch."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "import torch\\nimport torch.nn as nn\\nfrom src.models.model import DeepLearningModel\\n\\n# Set device\\ndevice = torch.device('cuda' if torch.cuda.is_available() else 'cpu')\\n\\n# Initialize model\\nmodel = DeepLearningModel().to(device)\\n\\n# Define loss and optimizer\\ncriterion = nn.MSELoss()\\noptimizer = torch.optim.Adam(model.parameters(), lr=0.001)\\n\\n# Training loop\\nfor epoch in range(100):\\n    model.train()\\n    for batch_idx, (data, target) in enumerate(train_loader):\\n        data, target = data.to(device), target.to(device)\\n        optimizer.zero_grad()\\n        output = model(data)\\n        loss = criterion(output, target)\\n        loss.backward()\\n        optimizer.step()\\n    \\n    if epoch % 10 == 0:\\n        print(f'Epoch {epoch}, Loss: {loss.item():.4f}')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}"""
        },
        ProjectTemplate.NLP: {
            os.path.join(project_name, "notebooks", "01_text_preprocessing.ipynb"): """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# NLP Text Preprocessing\\n\\nThis notebook demonstrates text preprocessing techniques for NLP tasks."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "from src.data.preprocessing import preprocess_text\\nimport pandas as pd\\n\\n# Load text data\\ntexts = pd.read_csv('../data/raw/texts.csv')['text']\\n\\n# Preprocess texts\\nprocessed_texts = texts.apply(preprocess_text)\\n\\n# Display example\\nprint('Original text:')\\nprint(texts[0])\\nprint('\\nProcessed text:')\\nprint(processed_texts[0])"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}""",
            os.path.join(project_name, "notebooks", "02_model_training.ipynb"): """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# NLP Model Training\\n\\nThis notebook demonstrates how to train and use a transformer-based model."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "from src.models.model import NLPModel\\n\\n# Initialize model\\nmodel = NLPModel()\\n\\n# Example prediction\\ntext = 'This is an example sentence.'\\nprediction = model.predict(text)\\nprint('Prediction:', prediction)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}"""
        },
        ProjectTemplate.COMPUTER_VISION: {
            os.path.join(project_name, "notebooks", "01_image_preprocessing.ipynb"): """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Computer Vision Image Preprocessing\\n\\nThis notebook demonstrates image preprocessing techniques for computer vision tasks."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "from src.data.preprocessing import preprocess_image\\nimport matplotlib.pyplot as plt\\n\\n# Load and preprocess image\\nimage_path = '../data/raw/example.jpg'\\nprocessed_img = preprocess_image(image_path)\\n\\n# Display original and processed images\\nplt.figure(figsize=(12, 4))\\nplt.subplot(1, 2, 1)\\nplt.imshow(plt.imread(image_path))\\nplt.title('Original Image')\\nplt.subplot(1, 2, 2)\\nplt.imshow(processed_img)\\nplt.title('Processed Image')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}""",
            os.path.join(project_name, "notebooks", "02_model_training.ipynb"): """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Computer Vision Model Training\\n\\nThis notebook demonstrates how to train and use a computer vision model."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "import torch\\nfrom src.models.model import VisionModel\\n\\n# Initialize model\\nmodel = VisionModel(num_classes=10)\\n\\n# Example prediction\\nimage = torch.randn(1, 3, 224, 224)  # Example input\\nprediction = model(image)\\nprint('Prediction shape:', prediction.shape)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}"""
        }
    }

    template_files = {
        ProjectTemplate.BASIC: {
            os.path.join(project_name, "src", "models", "model.py"): """# Basic ML model implementation
from sklearn.base import BaseEstimator

class Model(BaseEstimator):
    def __init__(self):
        self.model = None
    
    def fit(self, X, y):
        # Implement training logic
        pass
    
    def predict(self, X):
        # Implement prediction logic
        pass
""",
            os.path.join(project_name, "src", "data", "preprocessing.py"): """# Data preprocessing utilities
import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    # Implement preprocessing steps
    return data
""",
        },
        ProjectTemplate.DEEP_LEARNING: {
            os.path.join(project_name, "src", "models", "model.py"): """# Deep Learning model implementation
import torch
import torch.nn as nn

class DeepLearningModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(10, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )
    
    def forward(self, x):
        return self.layers(x)
""",
            os.path.join(project_name, "src", "models", "train.py"): """# Training script
import torch
from torch.utils.data import DataLoader

def train(model, train_loader: DataLoader, criterion, optimizer, device):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
""",
        },
        ProjectTemplate.NLP: {
            os.path.join(project_name, "src", "models", "model.py"): """# NLP model implementation
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class NLPModel:
    def __init__(self, model_name="bert-base-uncased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
    
    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        outputs = self.model(**inputs)
        return outputs.logits
""",
            os.path.join(project_name, "src", "data", "preprocessing.py"): """# NLP preprocessing utilities
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def preprocess_text(text: str) -> str:
    # Download required NLTK data
    nltk.download('punkt')
    nltk.download('stopwords')
    
    # Tokenize and remove stopwords
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    return ' '.join(tokens)
""",
        },
        ProjectTemplate.COMPUTER_VISION: {
            os.path.join(project_name, "src", "models", "model.py"): """# Computer Vision model implementation
import torch
import torch.nn as nn
import torchvision.models as models

class VisionModel(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.model = models.resnet18(pretrained=True)
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)
    
    def forward(self, x):
        return self.model(x)
""",
            os.path.join(project_name, "src", "data", "preprocessing.py"): """# Computer Vision preprocessing utilities
import cv2
import numpy as np

def preprocess_image(image_path: str, target_size=(224, 224)) -> np.ndarray:
    # Read and preprocess image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    img = img / 255.0  # Normalize
    return img
""",
        }
    }

    # Combine base files with template-specific files and notebooks
    files = base_files.copy()
    files.update(template_files.get(template, {}))
    files.update(notebook_templates.get(template, {}))
    return files

def create_ml_project_structure(project_name="my_ml_project", template: ProjectTemplate = ProjectTemplate.BASIC):
    """
    Creates a standard machine learning project file structure and sets up a virtual environment.    
    Args:
        project_name (str): The name of the project directory.
        template (ProjectTemplate): The type of ML project template to use.
    """
    
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # Define the directories to create
    dirs = [
        os.path.join(project_name, "data", "raw"),
        os.path.join(project_name, "data", "processed"),
        os.path.join(project_name, "data", "external"),
        os.path.join(project_name, "data", "interim"),
        os.path.join(project_name, "models","logs"),
        os.path.join(project_name, "notebooks"),
        os.path.join(project_name, "src", "data"),
        os.path.join(project_name, "src", "models"),
        os.path.join(project_name, "src", "utils"),
        os.path.join(project_name, "reports","figures"),
        os.path.join(project_name, "config"),
        os.path.join(project_name, "tests"),
        os.path.join(project_name, "scripts"),
        os.path.join(project_name, "docker"),
    ]

    try:
        # Create the directories
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
    
        # Create essential files with template-specific content
        files = {
            os.path.join(project_name, "requirements.txt"): "\n".join(get_template_dependencies(template)),
            os.path.join(project_name, "README.md"): f"""# {project_name}

## Project Description:
This is a {template.value} machine learning project.

## Installation:
```bash
pip install -r requirements.txt
```

## Usage:
1. Activate the virtual environment
2. Run the training script
3. Check the results in the reports directory

## Project Structure:
- `data/`: Data storage
- `models/`: Trained models
- `notebooks/`: Jupyter notebooks
- `src/`: Source code
- `config/`: Configuration files
- `tests/`: Unit tests
- `reports/`: Project reports
""",
            os.path.join(project_name, ".gitignore"): """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/

# IDEs
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
data/raw/*
data/processed/*
data/external/*
data/interim/*
models/*
!models/.gitkeep
""",
            os.path.join(project_name, "config", "config.yaml"): f"""# Project Configuration
project_name: {project_name}
template: {template.value}

# Data paths
data:
  raw: data/raw
  processed: data/processed
  external: data/external
  interim: data/interim

# Model parameters
model:
  type: {template.value}
  save_dir: models
  log_dir: models/logs

# Training parameters
training:
  batch_size: 32
  epochs: 100
  learning_rate: 0.001
""",
        }
        
        # Add template-specific files
        files.update(get_template_files(project_name, template))
        
        # Create files
        for file_path, content in files.items():
            with open(file_path, "w") as f:
                f.write(content)

        logging.info(f"✅ Project structure '{project_name}' created successfully with {template.value} template.")

        # Create virtual environment
        create_virtual_environment(project_name)
    
    except Exception as e:
        logging.error(f"❌ Error creating project: {e}")
        sys.exit(1)

def create_virtual_environment(project_name):
    """Creates a virtual environment inside the project directory."""
    venv_path = os.path.join(project_name, "venv")

    try:
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        logging.info(f"✅ Virtual environment created at '{venv_path}'.")
        logging.info(f"💡 Activate it using: \n -Windows: `{venv_path}\\scripts\\activate`\n -macOS/Linux: `source {venv_path}/bin/activate`")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Failed to create virtual environment: {e}")

def create_model_file(self, model_dir: Path, template_type: str) -> None:
    """Create model implementation file with docstrings and examples."""
    model_file = model_dir / "model.py"
    class_name = self._get_model_class_name(template_type)
    
    with open(model_file, "w") as f:
        f.write(get_docstring_template(class_name, "model"))
        f.write("\n\n")
        f.write(self._get_model_implementation(template_type))
        f.write("\n\n")
        f.write(get_example_code("model"))

def create_preprocessing_file(self, data_dir: Path) -> None:
    """Create preprocessing utilities with docstrings and examples."""
    preprocessing_file = data_dir / "preprocessing.py"
    
    with open(preprocessing_file, "w") as f:
        f.write(get_docstring_template("", "preprocessing"))
        f.write("\n\n")
        f.write(self._get_preprocessing_implementation())
        f.write("\n\n")
        f.write(get_example_code("preprocessing"))

def create_training_file(self, models_dir: Path) -> None:
    """Create training utilities with docstrings and examples."""
    training_file = models_dir / "training.py"
    
    with open(training_file, "w") as f:
        f.write(get_docstring_template("", "training"))
        f.write("\n\n")
        f.write(self._get_training_implementation())
        f.write("\n\n")
        f.write(get_example_code("training"))

def create_visualization_file(self, utils_dir: Path) -> None:
    """Create visualization utilities with docstrings and examples."""
    visualization_file = utils_dir / "visualization.py"
    
    with open(visualization_file, "w") as f:
        f.write(get_docstring_template("", "visualization"))
        f.write("\n\n")
        f.write(self._get_visualization_implementation())
        f.write("\n\n")
        f.write(get_example_code("visualization"))

def create_config_file(self, config_dir: Path) -> None:
    """Create configuration file with documentation."""
    config_file = config_dir / "config.py"
    
    with open(config_file, "w") as f:
        f.write(get_config_template())

def create_test_file(self, tests_dir: Path, template_type: str) -> None:
    """Create test file with documentation."""
    class_name = self._get_model_class_name(template_type)
    test_file = tests_dir / f"test_model.py"
    
    with open(test_file, "w") as f:
        f.write(get_test_template(class_name))


