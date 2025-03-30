from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cursofiap-package-temp',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib cursofiap',
    author='manoel',
    author_email='seu.email@example.com',
    url='https://github.com/ManoelSa/cursofiap2025',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
