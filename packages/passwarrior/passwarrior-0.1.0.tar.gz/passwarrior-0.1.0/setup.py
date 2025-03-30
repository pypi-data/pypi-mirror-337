import os
from setuptools import setup, find_packages

long_description = ''
if os.path.exists('README.md'):
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()

setup(
    name="passwarrior",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Your Name",
    author_email="mr.cheng.shi@gmail.com",
    description="A simple Python package for generating random passwords",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/C-Shi/passwarrior",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)