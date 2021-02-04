#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 16:24:19 2021

@author: tardis
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiv",
    version="0.3.29",
    author="tardis",
    author_email="nesegunes.ce@gmail.com",
    description="A variant annotation package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nesegunes/aiv",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['myvariant'],
)
