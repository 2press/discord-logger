# read the contents of README file
from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='discord-logger',
      version='0.0.1',
      description=('A Python logger to send information to Discord Webhooks.'),
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/2press/discord-logger',
      author='pressure',
      author_email='pres.sure@ymail.com',
      license='MIT',
      packages=['discord-logger'],
      install_requires=[
          'requests'
      ],
      zip_safe=False)
