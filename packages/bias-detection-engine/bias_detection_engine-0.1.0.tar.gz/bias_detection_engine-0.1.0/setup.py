from setuptools import setup, find_packages

setup(
    name="bias_detection_engine",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=0.24.0",
        "scipy>=1.7.0",
        "tensorflow>=2.6.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "plotly>=5.1.0",
    ],
    author="Ethan Zhang",
    author_email="ethanzhang@example.com",
    description="A tool for detecting biases in machine learning datasets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ethanzhang/bias_detection_engine",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 