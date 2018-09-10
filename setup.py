import setuptools
from delta_rest_client import __version__ as version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="delta_rest_client",
    version=version,
    author="Arbaaz",
    author_email="me@arbaaz.io",
    description="Rest Client for Delta Exchange",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/delta-exchange/python-rest-client",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
