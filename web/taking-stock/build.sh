#!/bin/sh

set -e

VENV_NAME="/tmp/buildenv"

echo "Making new env $VENV_NAME"
python3 -m venv $VENV_NAME
. "$VENV_NAME/bin/activate"

echo "Installing requirements"
pip install -r model/requirements.txt

cd model

echo "Making models..."

echo "  1/4 AAPL"
python3 stock.py WIKI/AAPL

echo "  2/4 AMZN"
python3 stock.py WIKI/AMZN

echo "  3/4 FB"
python3 stock.py WIKI/FB

echo "  4/4 GOOGL"
python3 stock.py WIKI/GOOGL

cd $OLDPWD

echo "Cleaning up"
deactivate
rm -rf $VENV_NAME

cp model/AAPL.joblib  src/models/AAPL
cp model/AMZN.joblib  src/models/AMZN
cp model/FB.joblib    src/models/FB
cp model/GOOGL.joblib src/models/GOOGL