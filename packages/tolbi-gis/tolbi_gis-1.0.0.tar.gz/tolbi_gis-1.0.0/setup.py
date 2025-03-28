from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tolbi-gis",
    version="1.0.0",  # Initial version
    packages=find_packages(),
    install_requires=[
        "Django>=3.2",
        "geopandas",
    ],
    author="Tolbi",
    author_email="dep.it@tolbico.com",
    description="A Django middleware to explode GeoJSON files in requests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
)
