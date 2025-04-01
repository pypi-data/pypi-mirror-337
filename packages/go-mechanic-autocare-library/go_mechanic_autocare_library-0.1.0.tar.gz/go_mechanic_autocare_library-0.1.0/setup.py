from setuptools import setup, find_packages

setup(
    name="go-mechanic-autocare-library",  # Unique package name on PyPI
    version="0.1.0",  # Versioning
    author="Mohan Morla",
    author_email="morlamohansai@gmail.com",
    description="A Python library for auto care tracking using DynamoDB",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),  # Automatically detect packages
    install_requires=[
        "boto3",  # Add dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
