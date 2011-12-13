#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Alisue
# Last Change:  18-Mar-2011.
#
from setuptools import setup, find_packages

version = "0.1rc7"

def read(filename):
    import os.path
    return open(os.path.join(os.path.dirname(__file__), filename)).read()
setup(
    name="django-object-permission",
    version=version,
    description = "Django's object permission library",
    long_description=read('README.rst'),
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords = "django permission object",
    author = "Alisue",
    author_email = "lambdalisue@hashnote.net",
    url=r"https://github.com/lambdalisue/django-object-permission",
    download_url = r"https://github.com/lambdalisue/django-object-permission/tarball/master",
    license = 'BSD',
    packages = find_packages(),
    include_package_data = False,
    zip_safe = True,
    install_requires=[
        'setuptools',
        ],
)
