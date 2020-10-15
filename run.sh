#!/bin/bash
if [ -d env ] ; then
    echo "ENV Found.."
    source env/bin/activate
else
    echo "ENV not found.. attempting to install... Please wait.."
    python3 -m venv env
    source env/bin/activate
    pip3 install -r bin/dependencies.txt
fi

python3 main.py