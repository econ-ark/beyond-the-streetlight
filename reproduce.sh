#!/bin/bash

# Get the script directory
SCPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)

cd "$SCPT_DIR"

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Please install Poetry first:"
    echo "curl -sSL https://install.python-poetry.org | python3 -"
    echo "Or visit: https://python-poetry.org/docs/#installation"
    exit 1
fi

# Install dependencies using Poetry
echo "Installing dependencies with Poetry..."
poetry install

# Check if installation was successful
if [ $? -ne 0 ]; then
    echo "Poetry install failed. Please check the error messages above."
    exit 1
fi

echo "Running reproduction workflow..."

# Run the Jupyter notebook
poetry run ipython *.ipynb

# Run the main reproduction script
poetry run python code/main/reproduce.py

echo "Reproduction workflow completed!"



