#!/usr/bin/env python

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from setuptools import setup, find_packages

setup(
    name='gravon',
    version='0.1.dev0',
    description='Data science toolkit for the Gravon archive of Stratego games',
    url='https://github.com/rhalbersma/gravon',
    author='Rein Halbersma',
    license='Boost Software License 1.0 (BSL-1.0)',
    packages=find_packages(where='src'),
    package_dir={'':'src'},
    install_requires=[
        'lxml', 'numpy', 'pandas'
    ],
    python_requires='>=3.6',
)
