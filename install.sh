#!/bin/bash

# Create a virtual environment in the "venv" folder
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Virtual environment created."
else
    echo "The virtual environment 'venv' already exists."
fi

# Activate the virtual environment
if [ "$(uname)" == "Darwin" ] || [ "$(uname)" == "Linux" ]; then
    # For Linux/macOS
    source .venv/bin/activate
    echo "Virtual environment activated for Linux/macOS."
elif [ "$(uname)" == "CYGWIN"* ] || [ "$(uname)" == "MINGW"* ] || [ "$(uname)" == "MSYS"* ]; then
    # For Windows
    source .venv/Scripts/activate
    echo "Virtual environment activated for Windows."
else
    echo "System unrecognized. Please activate the virtual environment manually."
    exit 1
fi

# Install required packages
pip install PyQt5 mysql-connector-python

echo "Packages PyQt5 and mysql-connector-python installed."

echo "The installation is complete."
