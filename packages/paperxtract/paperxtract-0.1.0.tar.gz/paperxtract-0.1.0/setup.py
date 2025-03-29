from setuptools import setup, find_packages
import os

# Read version information
with open(os.path.join('paperxtract', '__init__.py'), 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line)
            break

# Read README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="paperxtract",
    version=__version__,
    author="yuxiaoLee",
    author_email="yuxiaolee@foxmail.com",
    description="Academic Paper Extraction and Formatting Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuxiaoLeeMarks/paperxtract",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "openreview-py>=1.0",
        "pandas>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "paperxtract=paperxtract.cli:main",
        ],
    },
) 