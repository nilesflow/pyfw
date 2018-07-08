#!usr/bin/env python

from setuptools import setup, find_packages

setup(name = "pyfw",
    version = "0.0.2",
    description = "nilesflow: Personal Python Framework",
    url = "https://github.com/nilesflow/pyfw",
    author = "nilesflow",
    author_email = "nilesflow@gmail.com",
    license = "MIT",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
    packages = find_packages(),
)
