from setuptools import setup, find_packages

setup(
    name="voc2yolo",
    version="0.1.0",
    description="A simple Python package to convert Pascal VOC annotations to YOLO format.",
    author="Saikat Raj",
    author_email="saikat.raj.cs@gmail.com",
    url="https://github.com/Saikat-Raj/voc2yolo",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
