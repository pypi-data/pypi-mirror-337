from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'A Python Library for 3D Image Transformation.'
LONG_DESCRIPTION = 'This Python library provides a tool for 3D image transformations, including rotations and translations in 3D space. The transformations operate in three-dimensional space using sequential logic through the main class.'

# Setting up
setup(
    name="img3d",
    version=VERSION,
    author="Majid Alekasir",
    author_email="<majid.alekasir@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://github.com/OmidAlekasir/image_transformer',
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'image', 'transformation', 'translation', 'rotation', 'homography', '3D', 'spherical', 'roll', 'pitch', 'yaw', 'stabilization', 'coordinates'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
    ]
)