import os
from setuptools import setup, find_packages

setup(
    name="corex-storage-s3",
    version="0.1.1",
    author="Jochen Schultz",
    author_email="js@intelligent-intern.com",
    description="S3 storage handler implementation for CoreX using boto3",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "boto3>=1.17.0"
    ],
)
