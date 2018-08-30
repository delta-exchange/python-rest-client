#!/bin/sh -

rm -rf build dist delta_rest_client.egg-info
python3 setup.py sdist bdist_wheel
twine upload --repository pypi dist/*