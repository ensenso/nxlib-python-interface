from setuptools import setup
from os import path


# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='nxlib',
      packages=['nxlib'],
      python_requires='>3.5.0',  # from 3.5 numpy is default installed
      version='0.1',
      description='Python interface to interact with the Ensenso NxLib',
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 3 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Topic :: Text Processing :: Linguistic',
      ],
      url='https://git.ensenso.de/pub/nxlib-python-interface',
      author='Yasin Guenduez, Paul Rogister',
      author_email='yasin.guenduez@ensenso.com, paul.rogister@isys-vision.de',
      license='MIT',

      # Either cv or numpy is needed for image buffers
      install_requires=[
          'numpy'
      ],
      setup_requires=['pytest-runner', 'flake8', 'pep8-naming'],
      tests_require=['pytest'],
      zip_safe=False)
