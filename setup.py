import setuptools

setuptools.setup(
   name="bufkit-api",
   version="1.0.0",
   description="Provides a Python interface to BUFKIT BUFR files.",
   url="https://github.com/HumphreysCarter/bufkit-api",
   author="Carter Humphreys",
   packages=setuptools.find_packages(include=["bufkit*"])
)
