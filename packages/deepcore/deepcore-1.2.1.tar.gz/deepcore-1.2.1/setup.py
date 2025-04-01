from setuptools import setup, find_packages
import codecs
import os


with open("README.md", "r") as f:
    description = f.read()

setup(
    name="deepcore",
    version="1.2.1",
    packages=find_packages(),
    install_requires=[

    ],
    author="vishal singh",
    author_email="vishalsinghomr@gmail.com",
    keywords="measurement of central tendency, library, python , mean , ,median , mode, multimode",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ],
    python_requires=">=3.6",

    long_description=description,
    long_description_content_type="text/markdown",
)