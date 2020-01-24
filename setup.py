import setuptools

def readme():
    with open('README.md') as f:
        return f.read()

setuptools.setup(name='climate',
      version='0.1',
      description='A different way to create cli applicaitons',
      long_description=readme(),
      classifiers=[
           'Development Status :: 3 - Alpha',
           'License :: OSI Approved :: MIT License',
           'Programming Language :: Python :: 3.7',
           'Topic :: Text Processing :: Linguistic',
      ],
      url='http://github.com/fiddycodes/CliMate',
      author='Fidel Elie',
      author_email='fiddytypest@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
          'Pyinquirer'
      ],
      entry_points={
          'console_scripts': [
              'clm=climate.climate:main'
         ]
      },
      zip_safe=False,
      include_package_data=True)
