# Bias Detection Engine for ML Datasets

A comprehensive tool for detecting various types of biases in machine learning datasets before model training begins.

## Features

- **Predictive Imbalance Detection**: Identifies class imbalance and feature distribution skews
- **Label Leakage Analysis**: Detects potential data leakage and feature dependencies
- **Distributional Bias**: Analyzes demographic and categorical feature distributions
- **Information Theoretic Metrics**: Measures feature importance and mutual information
- **Autoencoder-based Anomaly Detection**: Identifies unusual patterns in the data
- **Contrastive Learning Analysis**: Evaluates feature representations and relationships

## Installation

```bash
pip install -r requirements.txt
```

## Project Structure

```
bias_detection_engine/
├── core/
│   ├── __init__.py
│   ├── imbalance_detector.py
│   ├── leakage_detector.py
│   ├── distribution_analyzer.py
│   └── feature_analyzer.py
├── utils/
│   ├── __init__.py
│   ├── preprocessing.py
│   └── visualization.py
├── models/
│   ├── __init__.py
│   ├── autoencoder.py
│   └── contrastive_learner.py
├── notebooks/
│   └── examples/
└── tests/
    └── __init__.py
```

## Usage

```python
from bias_detection_engine.core import ImbalanceDetector, LeakageDetector, DistributionAnalyzer
from bias_detection_engine.utils import preprocess_data

# Load and preprocess your dataset
data = preprocess_data(your_dataset)

# Detect imbalances
imbalance_detector = ImbalanceDetector()
imbalance_report = imbalance_detector.analyze(data)

# Check for label leakage
leakage_detector = LeakageDetector()
leakage_report = leakage_detector.analyze(data)

# Analyze distributions
distribution_analyzer = DistributionAnalyzer()
distribution_report = distribution_analyzer.analyze(data)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 