from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()
    

setup(
    name='debug2',
    version='0.1.0',    
    description='A debug Python package',
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
)