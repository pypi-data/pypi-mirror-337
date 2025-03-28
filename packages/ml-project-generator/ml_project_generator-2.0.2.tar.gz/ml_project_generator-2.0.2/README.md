# ML Project Generator

🚀 **ml-project-generator** (v2.0.0) is a powerful Python package that automates the creation of structured machine learning project templates. It helps you focus on development rather than setup by providing ready-to-use project structures with specialized templates for different ML domains.

## ✨ Features

### Project Templates

- **Basic ML**: Standard ML project structure with scikit-learn support
- **Deep Learning**: PyTorch-based project with neural network support
- **NLP**: Natural Language Processing project with transformers
- **Computer Vision**: Image processing project with PyTorch and OpenCV

### Each Template Includes

- 📁 Organized directory structure
- 📝 Example notebooks with step-by-step guides
- 🔧 Pre-configured dependencies
- 🛠 Template-specific utility functions
- 📊 Data preprocessing pipelines
- 🧪 Model training scripts
- 📈 Visualization utilities

### Project Structure

```
my_ml_project/
├── data/
│   ├── raw/          # Original data
│   ├── processed/    # Processed data
│   ├── external/     # External data sources
│   └── interim/      # Intermediate data
├── models/
│   └── logs/         # Training logs
├── notebooks/        # Example notebooks
├── src/
│   ├── data/         # Data processing scripts
│   ├── models/       # Model implementations
│   └── utils/        # Utility functions
├── config/           # Configuration files
├── reports/          # Project reports
├── tests/            # Unit tests
└── scripts/          # Automation scripts
```

## 📥 Installation

### From PyPI (Recommended)

```bash
pip install ml-project-generator
```

### From GitHub

```bash
pip install git+https://github.com/AarambhaAnta/ml-project-generator.git
```

### Development Installation

```bash
git clone https://github.com/AarambhaAnta/ml-project-generator.git
cd ml-project-generator
pip install -e .
```

## 🚀 Usage

### Basic Usage

```bash
ml-gen my_project
```

### With Template Selection

```bash
# Basic ML template (default)
ml-gen my_project

# Deep Learning template
ml-gen my_project --template deep_learning

# NLP template
ml-gen my_project --template nlp

# Computer Vision template
ml-gen my_project --template computer_vision
```

### With Virtual Environment

```bash
ml-gen my_project --venv
```

## 📚 Example Notebooks

Each template includes specialized notebooks:

### Basic ML

- Data exploration and analysis
- Model training and evaluation

### Deep Learning

- Data preparation and PyTorch setup
- Model training with PyTorch

### NLP

- Text preprocessing
- Transformer model training

### Computer Vision

- Image preprocessing
- Vision model training

## 🛠 Development

1. Clone the repository:

   ```bash
   git clone https://github.com/AarambhaAnta/ml-project-generator.git
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run tests:
   ```bash
   python -m pytest
   ```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the cookiecutter data science project template
- Built with ❤️ for the ML community

---

Made with ❤️ by [@AarambhaAnta](https://github.com/AarambhaAnta)
