from setuptools import setup, find_packages

setup(
    name = 'NLP_sentiment',
    version= '1.0.0',
    packages= find_packages(),
    install_requires = [
        'numpy >= 1.26.3'
    ],
)