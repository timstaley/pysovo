#!/usr/bin/env python

from setuptools import setup
import versioneer

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="pysovo",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=['pysovo', 'pysovo.comms', 'pysovo.triggers',
              'pysovo.tests', 'pysovo.tests.resources'],
    package_data={'pysovo':[
        'tests/resources/*.xml',
       'templates/*.j2', 'templates/includes/*.j2'
    ]},
    description="Utility scripts for reacting to received VOEvent packets",
    author="Tim Staley",
    author_email="timstaley337@gmail.com",
    url="https://github.com/timstaley/pysovo",
    install_requires=required
)
