import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='python-rest-model',
    url="https://github.com/mdaif/python-rest-model",
    version='1.0',
    packages=['rest_model', 'tests'],
    include_package_data=True,
    license='OSI Approved',  # example license
    description='A standard way to consume a RESTful service, inspired by Django models',
    long_description=README,
    author='Mohamed Daif',
    author_email='mohamed@daif.me',
    install_requires = ['requests==2.8.0'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
    ],
)
