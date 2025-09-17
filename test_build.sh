#!/bin/sh

pip uninstall gapprox 
trash dist build *.egg-info
python -m build
cd dist
pip install ./*.whl
python -c 'import gapprox as ga'
