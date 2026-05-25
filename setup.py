from setuptools import setup, find_packages

setup(
    name="iot_predictive_maintenance",
    version="0.1.0",
    description="IoT Predictive Maintenance Platform with PySpark and MLflow",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "pyspark>=3.5.0",
        "delta-spark>=3.0.0",
        "mlflow>=2.9.0",
        "scikit-learn>=1.3.0",
        "pandas>=2.1.0",
        "numpy>=1.26.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-spark>=0.6.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ]
    },
)