import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
VERSION = open(os.path.join(here, 'VERSION.txt')).read().strip()

requires = [
    ]

setup(name='adsorb',
      version=VERSION,
      description='Lightweight loose coupling library for Python. Add listeners to a named event '\
      'and call them from anywhere to collect their responses.',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        ],
      author='Kiran Jonnalagadda',
      author_email='jace@pobox.com',
      url='http://jace.github.com/adsorb/',
      keywords='event loose-coupling signal',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      test_suite='adsorb',
      install_requires = requires,
      )
