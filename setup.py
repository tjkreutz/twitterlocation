# -*- coding: utf-8 -*-
"""Setup file."""
from setuptools import setup
from setuptools import find_packages

setup(name='twitterlocation',
      version='0.1.0',
      description='Twitter Location Guesser',
      author='Tim Kreutz',
      author_email='tim.kreutz@uantwerpen.be',
      url='https://github.com/tjkreutz/twitterlocation',
      license='GPLv3',
      packages=find_packages(include=['twitterlocation', 'twitterlocation.*']),
      install_requires=['tweepy',
                        'googlemaps'],
      classifiers=[
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 3'],
      keywords='twitter location',
      zip_safe=True,
      python_requires='>=3')