# setup.py
from setuptools import setup, find_packages           # Imports library

with open("README.md", "r", encoding="utf-8") as fh:  # Opens the README.md file
    long_description = fh.read()                      # Reads the entire content of the README.md

setup(                                                # Calls the setup function from setuptools to configure the package

    name='quickutilz',                 # Specifies the name of the package
    version='0.1.0',                                  # Specifies the version number of the package
    packages=find_packages(),                         # Automatically finds all packages and subpackages within the project directory

    install_requires=[                                # Lists the dependencies that need to be installed when this package is installed
    ],                                                # In this case, there are no dependencies listed, represented by an empty list

    author="Nirmal Mahale",                           # Author of the package
    author_email="mahalenirmal@gmail.com",            # Author's email address

    description="A collection of utility functions for QuickWash projects.",  # Provides a short description of the package
    long_description=long_description,                # Sets the long description of the package using the content from the README.md file
    long_description_content_type="text/markdown",    # Specifies the content type of the long description as Markdown

    url="https://github.com/nirmal7030/QuickWash.git",  

    classifiers=[                                     # Lists classifiers that help categorize the package on PyPI
        "Programming Language :: Python :: 3",        # Indicates that the package is written in Python 3
        "License :: OSI Approved :: MIT License",     # Indicates that the package is licensed under the MIT License
        "Operating System :: OS Independent",         # Indicates that the package is platform-independent (works on any OS)
    ],

    python_requires='>=3.6',                          # Specifies the minimum Python version required to run the package
    include_package_data=False,                       # Indicates whether to include non-Python files (e.g., data files) in the package (set to False because there are no additional files to include)
)