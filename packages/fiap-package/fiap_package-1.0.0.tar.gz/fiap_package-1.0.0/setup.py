from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='fiap-package',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib cursofiap',
    author='Vitor',
    author_email='vitornd1@gmail.com',
    url='https://github.com/vitornogueirad/fiap',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
