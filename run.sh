#!/bin/bash

# Follow symlink to real path before execution
cd "$(dirname "$(realpath "$0")")"

# Set up environment, and install dependencies
if [ -d env ] ; then
    echo "ENV Found.."
    source env/bin/activate
else
    echo "ENV not found.. attempting to install... Please wait.."
    python3 -m venv env
    source env/bin/activate
    pip3 install -r dependencies.txt
fi

# Program entry point
python3 main.py
