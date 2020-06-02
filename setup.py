from setuptools import setup

setup(name='pyiat',
      version='0.2',
      description='Analyze Implicit Association Test',
      url='http://github.com/amillner/pyiat',
      author='Alex Millner',
      author_email='alexmillner@gmail.com',
      license='GPL',
      packages=['pyiat'],
      install_requires=['pandas','numpy'],
      zip_safe=False)