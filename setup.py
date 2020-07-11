import setuptools

def readme():
    with open('README.rst') as f:
        return f.read()

setuptools.setup(name='py-CliMate',
      version='0.1.1',
      description='Creating Cli Application With An Edge',
      long_description=readme(),
      classifiers=[
           'Development Status :: 3 - Alpha',
           'License :: OSI Approved :: MIT License',
           'Programming Language :: Python :: 3.7',
           'Topic :: Text Processing :: Linguistic',
      ],
      url='https://fidelelie.github.io/cliMate/',
      author='Fidel Elie',
      author_email='Fidel.Elie2@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
          'Pyinquirer',
          'Colorama',
          'Termcolor'
      ],
      entry_points={
          'console_scripts': [
              'clm=climate.climate:main'
         ]
      },
      zip_safe=False,
      include_package_data=True,
      python_requires='>=3.7',)
