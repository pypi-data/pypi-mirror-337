#-------------------------------------------------------------------------------#
#
#                         --- p y C o l d S t r e a m ---
#
#-------------------------------------------------------------------------------#

import os
from setuptools import setup, find_packages

with open(os.path.join("coldstream", "VERSION")) as file:
    version = file.read().strip()

def read_requirements():
    with open("requirements.txt") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="pycoldstream",
    description="Python ColdStream REST API Wrapper",
    license="MIT License",
    version=version,
    author="Diabatix nv",
    keywords="diabatix coldstream python api wrapper",
    packages=find_packages(include=["coldstream"]),
    install_requires=read_requirements(),
    url="https://github.com/diabatix/pycoldstream",
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)

