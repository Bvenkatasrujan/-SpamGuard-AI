from setuptools import setup, find_packages

setup(
    name="spamguard",
    version="1.0.0",
    description="SpamGuard AI: Reusable Hybrid NLP Spam Detection & Security Engine",
    author="SpamGuard AI Team",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "scikit-learn>=1.3.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "joblib>=1.3.0",
        "nltk>=3.8.1"
    ],
    entry_points={
        "console_scripts": [
            "spamguard=spamguard.__main__:main"
        ]
    }
)
