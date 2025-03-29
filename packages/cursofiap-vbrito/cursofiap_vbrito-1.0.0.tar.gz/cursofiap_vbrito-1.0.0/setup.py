from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cursofiap-vbrito',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib cursofiap',
    author='Valmison Brito',
    author_email='valmisonbrito@gmail.com',
    url='https://github.com/Valmisonds/PT_FIAP_ML',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
