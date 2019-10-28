from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='ensenso_nxlib',
      packages=['ensenso_nxlib'],
      python_requires='>3.5.0',
      version='0.2',
      description='Python interface to interact with the Ensenso NxLib',
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3'
      ],
      url='https://github.com/ensenso/nxlib-python-interface.git',
      author='Yasin Guenduez, Paul Rogister',
      author_email='yasin.guenduez@ensenso.com, paul.rogister@isys-vision.de',
      license='MIT',
      install_requires=[
          'numpy'
      ],
      tests_require=['pytest'],
      zip_safe=False,
      extras_require={
          'dev': [
              'pytest-runner',
              'flake8',
              'pep8-naming'
          ]
      }
      )
