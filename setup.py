#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='trailmap',
      version='0.0.1',
      description='Acquisition Pathway Analysis tool for Cyclus',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Katie Mummah',
      author_email='katiemummah@gmail.com',
      url='https://github.com/CNERG/trailmap',
      packages=find_packages()
      )
