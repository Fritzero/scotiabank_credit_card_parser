#!/usr/bin/env python

from setuptools import setup, find_packages
reqs = [
    "pypdf2",
    "click"
]

setup(
    name="scotiabank-helper",
    version="1.0",
    packages=find_packages(exclude=('tests')),
    install_requires=reqs,
    author="Robert Fritze",
    author_email="r.fritze@utoronto.ca",
    entry_points={'console_scripts': ['scotiabank-helper = scotiabank_helper.cli:cli']}
)
