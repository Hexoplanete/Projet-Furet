#!/bin/bash

# Setup python path
os=`uname -o`
if [[ $1 != "" ]] then python=$1
else
    if [[ $os == "GNU/Linux" ]] then python=python3
    else python=python
    fi
fi

# Goto root directory
cd "$(dirname "$(realpath "$0")")/.."

echo "Creating virtual environment..."
$python -m venv .venv
if [[ $? != 0 ]] then
    echo "Failed to create virtual environment"
    echo "Exiting"
    exit 0
fi

echo "Activating virtual environment..."
if [[ $os == "GNU/Linux" ]] then source ./.venv/bin/activate
else source ./.venv/Scripts/activate
fi
if [[ $? != 0 ]] then
    echo "Failed to activate venv"
    echo "Exiting"
    exit 0
fi

echo "Installing dependencies..."
pip install uv && uv sync
if [[ $? != 0 ]] then
    echo "Failed to install dependencies"
    echo "Exiting"
    exit 0
fi

echo "Successfully setup furet environment"