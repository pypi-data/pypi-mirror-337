from setuptools import setup, find_packages

setup(
    name="carrotclient",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="CarrotClient",
    author_email="suport@carrotclient.com",
    description="This is a simple python module",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)