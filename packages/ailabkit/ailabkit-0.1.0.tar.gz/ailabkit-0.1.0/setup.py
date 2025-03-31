
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="ailabkit",
    version="0.1.0",
    description="AI Learning Lab Toolkit for classrooms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Michael Borck",
    author_email="michael@borck.me",
    url="https://github.com/teaching-repositories/ailabkit",
    packages=find_packages(),
    install_requires=[
        "typer",
        "requests",
        "python-fasthtml",
        "python-docx", 
        "pymupdf", 
        "scikit-learn", 
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
