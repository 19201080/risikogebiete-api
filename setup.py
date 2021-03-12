#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'Click>=7.0',
    'pdfminer.six==20201018',
    'requests==2.25.1',
    'beautifulsoup4==4.9.3',
    'aiofiles==0.6.0',
    'aiohttp==3.7.4',
    'country_list==0.2.1',
    'iso3166==1.0.1',
    'aiocsv==1.1.1',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

description = ('An API for the countries classified as risk areas '
               'by Germany in the context of SARS-CoV-2.')

setup(
    author="19201080",
    author_email='1920@10.80',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description=description,
    entry_points={
        'console_scripts': [
            'risikogebiete_api=risikogebiete_api.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='risikogebiete_api',
    name='risikogebiete_api',
    packages=find_packages(include=[
        'risikogebiete_api',
        'risikogebiete_api.*']
    ),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/19201080/risikogebiete-api',
    version='0.1.0',
    zip_safe=False,
)
