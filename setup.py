#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()


setup(
    name="vumi-http-proxy",
    version="0.1",
    description=(
        "HTTP Proxy in Python Twisted to prevent unauthorized access to "
        "blacklisted ips"),
    long_description=readme,
    author="Praekelt Foundation",
    author_email='dev@praekeltfoundation.org',
    url='https://github.com/praekelt/vumi-http-proxy',
    packages=find_packages() + [
        'twisted.plugins',
    ],
    package_data={'twisted.plugins': ['twisted/plugins/*.py']},
    include_package_data=True,
    install_requires=[
        'zope.interface',
        'Click',
        'Twisted',
    ],
    entry_points='''
        [console_scripts]
        clickme=vumi_http_proxy.clickme:cli
    ''',
    license="BSD",
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
