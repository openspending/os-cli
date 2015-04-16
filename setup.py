from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# from __future__ import unicode_literals

import os
import io
import json
from setuptools import setup, find_packages


DIR = os.path.abspath(os.path.dirname(__file__))
README = 'README.md'
METADATA = 'METADATA'
LICENSE = 'LICENSE'
README_PATH = os.path.join(DIR, README)
METADATA_PATH = os.path.join(DIR, METADATA)


with io.open(README_PATH, mode='r+t', encoding='utf-8') as stream:
    long_description = stream.read()


with io.open(METADATA_PATH, mode='r+t', encoding='utf-8') as stream:
    metadata = json.loads(stream.read())


dependencies = [
    'click',
    'requests',
    'requests-futures',
    'goodtables',
    'jtskit',
    'datapackage',
    'budgetdatapackage',
    'tabulate',
    'boto'
]


classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

setup(
    name=metadata['name'],
    version=metadata['version'],
    description=metadata['description'],
    long_description=long_description,
    author=metadata['author'],
    author_email=metadata['author_email'],
    url=metadata['url'],
    license=metadata['license'],
    packages=find_packages(exclude=['examples', 'tests']),
    package_data={'': [README, METADATA, LICENSE]},
    package_dir={metadata['slug']: metadata['slug']},
    include_package_data=True,
    install_requires=dependencies,
    zip_safe=False,
    keywords=metadata['keywords'],
    classifiers=classifiers,
    entry_points={
        'console_scripts': [
            'openspending = oscli.main:cli',
            'os = oscli.main:cli'
        ]
    }
)
