#!/bin/bash

echo "Setting up Beyond the Streetlight repository..."

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Add Poetry to PATH for this session
    export PATH="$HOME/.local/bin:$PATH"
    
    # Check if installation was successful
    if ! command -v poetry &> /dev/null; then
        echo "Poetry installation failed. Please install Poetry manually:"
        echo "Visit: https://python-poetry.org/docs/#installation"
        exit 1
    fi
    
    echo "Poetry installed successfully!"
else
    echo "Poetry is already installed."
fi

# Install dependencies
echo "Installing dependencies..."
poetry install

if [ $? -eq 0 ]; then
    echo "✅ Setup complete! You can now run:"
    echo "   ./reproduce.sh    # Run the full reproduction workflow"
    echo "   poetry shell      # Activate the Poetry environment"
    echo "   poetry run python code/main/reproduce.py  # Run manually"
else
    echo "❌ Setup failed during dependency installation."
    exit 1
fi 