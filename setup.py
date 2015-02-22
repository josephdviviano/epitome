from setuptools import setup

setup(name='epitome',
      version='0.2',
      description='A MRI metapipeline',
      url='https://github.com/josephdviviano/epitome',
      author='Joseph D Viviano',
      author_email='joseph@viviano.ca',
      license='Apache2.0',
      packages=['epitome'],
      scripts=['bin/epi-folder',
               'bin/epi-lowpass', 
               'bin/epi-physio',
               'bin/epi-queue'
               'bin/epi-sharc',
               'bin/epi-trdrop', 
               'bin/epitome'],
      zip_safe=False)
