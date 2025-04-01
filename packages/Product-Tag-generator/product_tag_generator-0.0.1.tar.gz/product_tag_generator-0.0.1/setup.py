# setup.py
from setuptools import setup, find_packages

setup(
    name='Product_Tag_generator',   # Package name
    version='0.0.1',
    description='A simple library to extract tags from product titles',
    long_description=open('USAGE.md').read(),
    long_description_content_type='text/markdown',
    author='Akash Venkatesan',
    author_email='akashv1006@gmail.com',
    packages=find_packages(),
    install_requires=[],
    license='MIT',
    python_requires='>=3.7',
)
    
