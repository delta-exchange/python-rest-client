import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="delta_rest_client",
    version="0.0.5",
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
