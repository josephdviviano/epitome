from setuptools import setup

setup(name='EPItome-xl',
      version='0.2',
      description='A MRI pre-processing pipeline',
      url='https://github.com/josephdviviano/EPItome-xl',
      author='Joseph D Viviano',
      author_email='joseph.d.viviano@gmail.com',
      license='MIT',
      packages=['epitome'],
      scripts=['bin/EPItome', 'bin/EPIphysio', 'bin/EPIfolder', 'bin/EPIqueue'],
      zip_safe=False)
