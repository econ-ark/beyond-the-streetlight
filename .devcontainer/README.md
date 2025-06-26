# Dev Container Configuration

This directory contains the VS Code / Cursor Dev Container configuration for the "Beyond the Streetlight" economic analysis project.

## What is a Dev Container?

A development container (or dev container for short) allows you to use a container as a full-featured development environment. This dev container is configured to provide:

- **Consistent Environment**: Identical development setup across all machines
- **Pre-installed Dependencies**: All Python packages and tools ready to use
- **IDE Integration**: VS Code/Cursor extensions automatically installed
- **Port Forwarding**: Jupyter Lab accessible at http://localhost:8888

## Prerequisites

1. **VS Code or Cursor** with the **"Dev Containers"** extension installed
2. **Docker Desktop** running on your machine

## Usage

### Automatic Detection (Recommended)

When you open this repository in VS Code/Cursor with the Dev Containers extension installed:

1. VS Code/Cursor will detect the `.devcontainer/devcontainer.json` file
2. A popup will appear asking "Reopen in Container"
3. Click "Reopen in Container" to build and start the dev environment
4. The first build may take several minutes

### Manual Commands

You can also use the Command Palette (`Ctrl+Shift+P`):

- **"Dev Containers: Reopen in Container"** - Build and open in container
- **"Dev Containers: Rebuild Container"** - Rebuild if configuration changes
- **"Dev Containers: Open Folder in Container"** - Open specific folder

## What's Included

### Pre-installed Extensions
- Python support with IntelliSense
- Jupyter notebook support
- Code formatting (Black, isort)
- Linting (Flake8, Ruff)
- TOML support for pyproject.toml

### Environment Setup
- Poetry virtual environment activated
- All project dependencies installed
- Environment variables configured
- Output directories mounted for persistence

### Quick Start Commands

Once inside the container:

```bash
# Run the full analysis
./reproduce.sh

# Run analysis only (faster)
./run_analysis.sh  

# Start Jupyter Lab
poetry run jupyter lab --ip=0.0.0.0 --port=8888 --allow-root

# Interactive Python shell
poetry run python
```

## File Persistence

The following directories are mounted to persist results outside the container:
- `results/` - Analysis results and outputs
- `figures/` - Generated plots and figures  
- `data/output/` - Processed data files

This means your analysis results will be preserved even if you rebuild the container.

## Troubleshooting

**Container won't build?**
- Make sure Docker Desktop is running
- Try "Dev Containers: Rebuild Container" from Command Palette

**Python imports not working?**
- The container sets `PYTHONPATH=/app` automatically
- Poetry virtual environment should be activated by default

**Jupyter Lab not accessible?**
- Check that port 8888 is forwarded (should be automatic)
- Visit http://localhost:8888 in your browser 