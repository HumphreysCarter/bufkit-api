from setuptools import setup, find_packages

setup(
   name="bufkit-api",
   version="1.0.0",
   description="Provides a Python interface to BUFKIT BUFR files.",
   url="https://github.com/HumphreysCarter/bufkit-api",
   author="Carter Humphreys",
   packages=find_packages(),
   package_dir={'bufkit': 'src/bufkit'},
   install_requires=[
      'metpy',
   ],
   python_requires='>=3.9',
)
