#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as req_file:
    requirements = req_file.read().split('\n')

with open('requirements-dev.txt') as req_file:
    requirements_dev = req_file.read().split('\n')

with open('VERSION') as fp:
    version = fp.read().strip()

setup(
    name="vumi-http-proxy",
    version=version,
    description="HTTP Proxy in Python Twisted to prevent unauthorized access to blacklisted ips",
    long_description=readme,
    author="Carla Wilby",
    author_email='thisiscarlawilby@gmail.co.za',
    url='https://github.com/praekelt/vumi-http-proxy',
    packages=[
        find_packages(),
    ],
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
