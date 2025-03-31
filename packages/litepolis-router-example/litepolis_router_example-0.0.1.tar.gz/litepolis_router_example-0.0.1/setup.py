# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='litepolis-router-example',
    version="v0.0.1",
    description='An example how to create API router module for LitePolis.',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='David',
    # author_email='Optional',                            # Change
    url='https://github.com/LitePolis-router-example',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['fastapi'],
)
