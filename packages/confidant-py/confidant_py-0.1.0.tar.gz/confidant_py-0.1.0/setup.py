from setuptools import setup, find_packages

setup(
    name="confidant-py",
    version="0.1.0",
    author="Vaibhav",
    author_email="shuklavaibhav336@gmail.com",
    description="Multi platform scalable environment variables manager.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mr-vaibh/confidant-py",
    packages=find_packages(),
    install_requires=[
        "cryptography"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
