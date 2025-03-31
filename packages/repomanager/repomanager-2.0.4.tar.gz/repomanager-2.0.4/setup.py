import os
import codecs
from setuptools import setup, find_packages

# Base directory of package
here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


# Get version without importing the package
with open(os.path.join(here, 'repomanager', '__init__.py'), 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('\'"')
            break

#Long Description
with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name="repomanager",
    version=version,
    description="Git Repository Manager",
    long_description=long_description,
    classifiers=[
          "Programming Language :: Python :: 3.8",
          "License :: OSI Approved :: BSD License",
          "Development Status :: 4 - Beta"
    ],
    url='https://gitlab.incoresemi.com/utils/repomanager',
    author='InCore Semiconductors Pvt. Ltd.',
    author_email='info@incoresemi.com',
    license='BSD-3-Clause',
    packages=find_packages(),
    package_dir={'repomanager': 'repomanager/'},
    package_data={},
    install_requires=[],
    python_requires='>=3.8.0',
    entry_points={
        'console_scripts': ['repomanager=repomanager.main:main'],
    },
    keywords='repomanager',
    zip_safe=False,
)
