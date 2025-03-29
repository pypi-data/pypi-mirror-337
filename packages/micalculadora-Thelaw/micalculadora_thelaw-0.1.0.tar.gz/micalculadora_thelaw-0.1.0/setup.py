from setuptools import setup, find_packages

#Leer el contenido del archivo README.md

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="micalculadora_Thelaw",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Thelaw",
    description="Un paquete de operaciones matematicas basicas.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/micalculadora/"


)
