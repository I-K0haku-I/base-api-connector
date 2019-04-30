from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='base-api-connector',
    version='0.1.1',
    description='Generic Connector so you can create simple and readable classes for accessing APIs.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/I-K0haku-I/base-api-connector',
    author='Andreas Schäfer',
    author_email=None,
    packages=find_packages(),
    install_requires=['requests']
)
