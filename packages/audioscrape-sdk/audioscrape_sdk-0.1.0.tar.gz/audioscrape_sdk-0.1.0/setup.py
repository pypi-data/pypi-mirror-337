from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="audioscrape-sdk",
    version="0.1.0",
    author="Audioscrape Team",
    author_email="support@audioscrape.com",
    description="Official Python SDK for Audioscrape API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/audioscrape/python-sdk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
)
