#!/usr/bin/env python
from setuptools import find_packages, setup

version = '0.1.0'

setup(
    name="rebase-chain",
    author="Andrew Mains",
    author_email="amains@uber.com",
    description="Script to deal with chains of git branches",
    version=version,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rebase-chain = branch_chain.rebase_chain:main'
        ]
    }
)
