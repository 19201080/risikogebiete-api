#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    'pdfminer.six',
    'requests',
    'beautifulsoup4',
    'aiofiles',
    'aiohttp',
    'country_list',
    'iso3166',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="19201080",
    author_email='1920@10.80',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="-",
    entry_points={
        'console_scripts': [
            'risikogebiete_analysis=risikogebiete_analysis.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='risikogebiete_analysis',
    name='risikogebiete_analysis',
    packages=find_packages(include=[
        'risikogebiete_analysis',
        'risikogebiete_analysis.*']
    ),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/19201080/risikogebiete_analysis',
    version='0.1.0',
    zip_safe=False,
)
