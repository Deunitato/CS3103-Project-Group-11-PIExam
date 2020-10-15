#!/bin/sh
python3 -m venv env
source env/bin/activate
pip install -r bin/dependencies.txt
python main.py