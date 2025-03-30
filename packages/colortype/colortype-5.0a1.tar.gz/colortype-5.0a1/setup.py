from setuptools import setup, find_packages
import os

# Read README
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Try reading CHANGELOG.md (optional)
if os.path.exists("CHANGELOG.md"):
    with open("CHANGELOG.md", encoding="utf-8") as f:
        long_description += "\n\n" + f.read()

setup(
    name="colortype",
    version="5.0a1",
    author="k_noob",
    author_email="k.noob1517@gmail.com",
    description="A simple ANSI color formatting library for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)