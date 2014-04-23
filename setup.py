#!/usr/bin/env python

from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="pysovo",
    version="0.4.0",
    packages=['pysovo', 'pysovo.comms',
              'pysovo.tests', 'pysovo.tests.resources'],
    package_data={'pysovo':['tests/resources/*.xml', 'templates/*.txt']}, 
    description="Utility scripts for reacting to received VOEvent packets",
    author="Tim Staley",
    author_email="timstaley337@gmail.com",
    url="https://github.com/timstaley/pysovo",
    install_requires=required
)
