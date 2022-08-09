#!/usr/bin/env python

"""Setup script"""

import setuptools

name = "qrestic"
version = "0.0.0"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().split()

packages = (
    [name]
    + [name + "." + p for p in setuptools.find_packages(where="./" + name)]
)

setuptools.setup(
    author="Cédric Ho Thanh",
    author_email="altaris@users.noreply.github.com",
    description="A simple GUI for restic",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    name=name,
    packages=packages,
    platforms="any",
    project_urls={
        "Issues": "https://github.com/altaris/qrestic/issues",
    },
    python_requires=">=3.8",
    url="https://github.com/altaris/qrestic",
    version=version,
)
