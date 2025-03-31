from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name='testingvaleria',
    version='1.0.2',
    packages=find_packages(),
    description='Uma biblioteca para análise de investimentos',
    author='Valeriateste',
    author_email='valeria.souzadsantos@gmail.com',
    url='https://github.com/testevaleria/valeriatesting',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown' 
)