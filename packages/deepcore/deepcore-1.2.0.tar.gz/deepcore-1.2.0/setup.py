from setuptools import setup, find_packages
import codecs
import os


with open("README.md","r") as f:
    description = f.read()

setup(
    name="deepcore",
    version="1.2.0",
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    author="vishal singh",
    author_email="vishalsinghomr@gmail.com",
    description="A short description of your library",
    keywords="measurement of central tendency, library, python , mean , ,median , mode, multimode",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ],
    python_requires=">=3.6",
)