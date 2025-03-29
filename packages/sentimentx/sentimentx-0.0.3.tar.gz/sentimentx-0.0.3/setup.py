from setuptools import setup, find_packages

setup(
    name="sentimentx",
    version="0.0.3",
    packages=find_packages(),
    install_requires=[
        "textblob",
        "nltk",
        "text2emotion",
        "stanza",
        "transformers",
        "torch"
    ],
    author="Vansh Gautam",
    description="A powerful sentiment analysis library combining lexicon and deep learning methods.",
    url="https://github.com/yourusername/sentimentx",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
