#!/bin/sh

# Setup python path
os=`uname -o`
if [ -n "$1" ]; then python="$1"
else
    if [ "$os" = "GNU/Linux" ]; then python="python3"
    elif [ "$os" = "Darwin" ]; then python="python3"
    else python="python"
    fi
fi

# Goto root directory
cd "$(dirname "$(realpath "$0")")/.."

echo "Creating virtual environment..."
$python -m venv .venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment"
    echo "Exiting"
    exit 0
fi

echo "Activating virtual environment..."
if [ "$os" = "GNU/Linux" ]; then . ./.venv/bin/activate
elif [ "$os" = "Darwins" ]; then . ./.venv/bin/activate
else . ./.venv/Scripts/activate
fi
if [ $? -ne 0 ]; then
    echo "Failed to activate venv"
    echo "Exiting"
    exit 0
fi

echo "Installing dependencies..."
pip install uv && uv sync
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies"
    echo "Exiting"
    exit 0
fi

echo "Successfully setup furet environment"