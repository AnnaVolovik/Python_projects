# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='just_another_parser_v1',
    version='0.0.1',
    author='Anna Volovik',
    author_email='anna_volovik@hotmail.com',
    description='Simple web parser counting number of tags on a specified url page',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    )
