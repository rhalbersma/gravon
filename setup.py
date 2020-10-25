#!/usr/bin/env python

#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from setuptools import setup, find_packages

setup(
    name='gravon',
    version='0.1.0-dev0',
    description='Data science tools for the Gravon archive of Stratego games and results',
    url='https://github.com/rhalbersma/gravon',
    author='Rein Halbersma',
    license='Boost Software License 1.0 (BSL-1.0)',
    packages=find_packages(where='src'),
    package_dir={'':'src'},
    package_data={
        'gravon': ['data/*.pkl'],
    },    
    install_requires=[
        'bs4', 'IPython', 'lxml', 'notebook', 'numpy', 'pandas', 'plotnine', 'pylint', 'requests', 'tqdm'
    ],
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
