from setuptools import setup, find_packages

setup(
    name="HumanTone",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
    "transformers",
    "textblob",
    "nltk",
    "sentence-transformers",
    "pyttsx3",
    "torch",
    "scipy",
    "pandas"
    ],
    description="A human-like sentiment analysis library with paraphrasing and speech capabilities.",
    author="Vansh Gautam",
    author_email="vanshgautam2005@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
