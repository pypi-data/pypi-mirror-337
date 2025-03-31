from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cursofiap-rodrigojager',
    version='1.0.0',
    packages=find_packages(),
    description='Cursofiap',
    author='Rodrigo Jäger',
    author_email='rodrigojager@gmail.com',
    url='https://github.com/rodrigojager/cursofiap',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
