#!/bin/sh

pip uninstall gapprox
trash dist build *.egg-info
python -m build
python -m twine upload --repository testpypi dist/*
pip install -i https://test.pypi.org/simple/ gapprox
python -c 'import gapprox as ga'
