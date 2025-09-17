#!/bin/sh

pip uninstall gapprox
trash dist build *.egg-info
python -m build
python -m twine upload --repository pypi dist/*
pip install -i https://test.pypi.org/simple/ gapprox
python -m gapprox

