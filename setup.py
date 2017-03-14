#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='tcping',
    author='zhengxiaowai',
    author_email='h1x2y3awalm@gmail.com',
    url='https://github.com/kontspace/tcping',
    description='command line for tcp ping',
    long_description_markdown_filename='README.md',
    license='MIT',
    keywords='python tcp ping',
    scripts=['tcping.py'],
    install_requires=['six', 'click', 'prettytable'],
    setup_requires=setup_requires,
    entry_points={
        'console_scripts': ['tcping = tcping:main']
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2"
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "Topic :: System"
    ]
) 