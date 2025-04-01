from setuptools import setup, find_packages # type: ignore

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="testpackagegepmc",
    version="0.0.3",
    author="Mario Alberto Calderon Galeana",
    author_email="galeanama@gmail.com",
    description="Paquete de ejemplo para uso de funciones.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/galeanama/test_package_gep_mc",   
    packages=find_packages(),
    classifiers=["Operating System :: OS Independent"],
    install_requires=[],
    python_requires=">=3.7"
)