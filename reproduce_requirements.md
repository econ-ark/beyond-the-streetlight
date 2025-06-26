# Reproduction Requirements

This document describes the steps necessary to execute the "reproduce.sh" file to produce the main results of this repository.

## Option 1: Automatic Setup (Recommended)

1. Run the automatic setup script:
```bash
./install.sh
```

This script will:
- Install Poetry if not already installed
- Install all required dependencies
- Set up the project environment

2. Once setup is complete, run the reproduction workflow:
```bash
./reproduce.sh
```

## Option 2: Manual Setup

1. **Install Poetry** if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

For other installation methods, visit: https://python-poetry.org/docs/#installation

2. **Install Dependencies**:
```bash
poetry install
```

3. **Run the Analysis**:
```bash
./reproduce.sh
```

## What the Scripts Do

- `install.sh`: Automatically installs Poetry and all dependencies
- `reproduce.sh`: Runs the complete reproduction workflow
  - Automatically installs dependencies using Poetry
  - Executes the Jupyter notebook
  - Runs all analysis scripts in the correct order
  - Generates all results and figures

## Requirements

- Python 3.9 or higher
- Internet connection (for downloading dependencies and FRED data)

All other dependencies are managed automatically by Poetry based on the `pyproject.toml` configuration.