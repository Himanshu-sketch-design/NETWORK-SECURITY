'''
setup.py is a build script template distributed with Python's setuptools package, 
which is used to install and manage Python projects and their dependencies. It is 
the heart and center of Python projects installed with pip and is used for building
Python projects based on packages and their dependencies listed in the script.
'''

from setuptools import setup, find_packages
from typing import List
import os

try:
    with open('README.md') as f:
        long_description = f.read()
except Exception:
    long_description = ''

def get_requirements() -> List[str]:
    
    requirement:List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readline()
            for line in lines:
                requirements = line.strip()
                if requirements and requirements != '-e .':
                    requirement.append(requirements)
    except FileNotFoundError:
        print("File not found!")

setup(
    name='Network_Security', 
    packages=find_packages('.'), 
    version='1.0.0',  
    description='Project on Network Security',
    long_description=long_description,  
    author='Himanshu Rana',
    author_email='himanshurana5800@gmail.com',
    url='https://github.com/Himanshu-sketch-design/NETWORK-SECURITY',
    install_requires=get_requirements(),
    classifiers=[
        'Programming Language :: Python :: 3.10'
    ]
)