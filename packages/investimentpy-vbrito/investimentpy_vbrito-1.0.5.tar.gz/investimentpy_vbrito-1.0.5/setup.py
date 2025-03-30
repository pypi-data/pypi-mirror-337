from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='investimentpy-vbrito',
    version='1.0.5',
    packages=find_packages(),
    description='Uma biblioteca para análise de investimentos',
    author='Valmison Brito',
    author_email='valmisonbrito@gmail.com',
    url='https://github.com/Valmisonds/investimentpy',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown' 
)