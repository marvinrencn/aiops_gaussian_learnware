#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="aiops_gaussian_learnware",
    version="0.0.1",
    description="aiops learnware platform",
    author="Marvin Ren",
    python_requires=">=3.6",
    install_requires=['SQLAlchemy', 'mysql-connector-python'],
    packages=find_packages(exclude=["test", "test.*"]),
    test_suite="tests"
)
