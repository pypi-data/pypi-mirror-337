from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'sajilocv is a library based on opencv and mediapipe'
long_description = 'sajilocv has been developed by Beyond Apogee from Nepal, as part of their Robotics Education initiatives.'

# Setting up
setup(
	name="sajilocv",
	version=VERSION,
	author="Sudip Vikram(Beyond Apogee)",
	author_email="<admin@beyond-apogee.com>",
	description=DESCRIPTION,
	long_description_content_type="text/markdown",
	long_description=long_description,
	packages=find_packages(),
	install_requires=['opencv-python','mediapipe'],
	keywords=['opencv','beyond apogee','robotics nepal'],
	classifiers=[
		"Development Status :: 1 - Planning",
		"Intended Audience :: Developers",
		"Intended Audience :: Education",
		"Intended Audience :: Science/Research",
		"Programming Language :: Python :: 3",
		"Operating System :: Unix",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Microsoft :: Windows",
	]
)