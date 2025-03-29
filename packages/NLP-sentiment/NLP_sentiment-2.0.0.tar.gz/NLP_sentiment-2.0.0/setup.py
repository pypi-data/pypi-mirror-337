from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name = 'NLP_sentiment',
    version= '2.0.0',
    packages= find_packages(),
    install_requires = [
        'numpy >= 1.26.3'
    ],

    long_description=description,
    long_description_content_type= "text/markdown",
)