from setuptools import setup

setup(name='epitome',
      version='0.2',
      description='A MRI metapipeline',
      url='https://github.com/josephdviviano/epitome',
      author='Joseph D Viviano',
      author_email='joseph@viviano.ca',
      license='MIT',
      packages=['epitome'],
      scripts=['bin/epitome', 'bin/epiphysio', 'bin/epifolder', 'bin/epiqueue'],
      zip_safe=False)
