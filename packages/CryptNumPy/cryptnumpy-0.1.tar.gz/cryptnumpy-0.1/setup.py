from setuptools import setup, find_packages

import cryptnumpy as crp

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name="CryptNumPy",
    version=crp.__version__,
    description=crp.__about__,
    url=crp.__url__,
    author=crp.__author__,
    license=crp.__license__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'cryptography >= 41.0.4', 'pyarrow >= 14.0.1'],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"]
    },
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent"],
    python_requires='>=3.6',
)
