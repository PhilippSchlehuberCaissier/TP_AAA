#!/usr/bin/env python

from setuptools import setup

VERSION = "0.1"

with open("README.md") as fin:
    README = fin.read()

with open("LICENSE") as fin:
    LICENSE = fin.read()

URL = "https://github.com/PhilippSchlehuberCaissier/TP_AAA"

DOWNLOAD_URL = ""

CLASSIFIERS = [
    "License :: OSI Approved :: GPL 3.0",
    "Programming Language :: Python",
]

from setuptools.command.install import install

import subprocess

class InstallLocalPackage(install):
    def run(self):
        install.run(self)
        subprocess.call(
            ["python3", "./gvmagic/setup.py", "install"]
        )

setup(
    name="TP_AAA",
    version=VERSION,
    author="Philipp Schlehuber-Caissier",
    author_email="philipp@lrde.epita.fr",
    description="Travaux Pratique cours Automates, Algebre et Applications",
    license=LICENSE,
    url=URL,
    download_url=DOWNLOAD_URL,
    classifiers=CLASSIFIERS,
    py_modules=["tp_aaa"],
    cmdclass={ 'install': InstallLocalPackage }
)
