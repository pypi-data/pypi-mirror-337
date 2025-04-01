from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
        name='angre',
        version='0.1.0',
        packages=find_packages(),
        install_requires=[],
        author='Angre',
        description='Consultar cursos de H4U',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://hack4u.io',
)

