# Beyond the Streetlight

This repository provides an analysis of the trend in forecast errors made by the Tealbook/Greenbook (GB) and the Survey of Professional Forecasters (SPF) for measures of the unemployment rate and real growth in personal consumption expenditures from 1982 to 2017. Below is a brief description of the main data and code used to produce the main results of this exercise.

The data on forecasts for unemployment and consumption made by the [federal reserve (Tealbook/Greenbook)](https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/philadelphia-data-set) and the [mean across private forcasters](https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/mean-forecasts) are provided by the Philidelphia Fed. Data on [realized values of the forecasted variables](https://fred.stlouisfed.org/) are provided by the St. Louis Fed. The subfolder "data" contains the raw and cleaned versions of each of these datasets.

The subfolder "code/main" performs the "main" tasks of this exercise using the cleaned data. First, the GB and SPF data are used to compute a forecast for real growth in personal consumption expenditures starting in any given quarter. Next, the corresponding final measure of the same variable (PCE growth) is obtained from [FRED](https://fred.stlouisfed.org/). From there, the absolute value of the difference between the annual changes in observed and forecasted values is computed. Lastly, standard statistical techniques are used to analyze the trend in these GB and SPF absolute forecast errors. 

## Quick Start

### Option 1: Using VS Code/Cursor Dev Container (Easiest for Development)

If you use VS Code or Cursor with the **"Dev Containers"** extension:

1. Open this repository in VS Code/Cursor
2. When prompted, click **"Reopen in Container"**
3. The development environment will build automatically
4. Run `./reproduce.sh` once the container is ready

This provides the best development experience with full IDE integration.

### Option 2: Using Docker (Recommended - Command Line)

```bash
# Build and run the full reproduction
./docker-run.sh reproduce

# Or run just the analysis (faster)
./docker-run.sh analysis

# For interactive development with Jupyter Lab
./docker-run.sh jupyter  # Access at http://localhost:8888

# For an interactive shell
./docker-run.sh shell
```

**Prerequisites for Docker:**
- [Docker](https://www.docker.com/get-started) installed and running
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker)

### Option 3: Using Poetry (For Local Development)

### Prerequisites

- Python 3.9 or higher
- [Poetry](https://python-poetry.org/) for dependency management

### Installation

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone this repository and navigate to it:
```bash
git clone <repository-url>
cd beyond-the-streetlight
```

3. Install dependencies:
```bash
poetry install
```

### Running the Analysis

To reproduce the complete analysis, simply run:
```bash
./reproduce.sh
```

This script will:
- Automatically install all required dependencies using Poetry
- Execute the Jupyter notebook
- Run all analysis scripts in the correct order
- Generate all results and figures

### Manual Execution

You can also run individual components manually:

```bash
# Run the main reproduction script
poetry run python code/main/reproduce.py

# Run individual analysis scripts
poetry run python code/main/parse_GB_raw_data.py
poetry run python code/main/parse_SPF_raw_data.py
# ... etc
```

## Project Structure

The code file "reproduce.py" can be accessed to see the order in which these programs were run to produce the results. The code "reproduce.sh" will allow the user to reproduce the results from the terminal.

## Dependencies

All dependencies are managed through Poetry and specified in `pyproject.toml`. Key dependencies include:
- pandas, numpy, matplotlib for data analysis and visualization
- statsmodels for statistical analysis
- fredapi and fredpy for Federal Reserve Economic Data access
- jupyterlab for notebook execution

## Docker Usage

### Docker Commands

The repository includes Docker support for maximum reproducibility and ease of use:

```bash
# View available Docker commands
./docker-run.sh help

# Build the Docker image
./docker-run.sh build

# Run the complete reproduction workflow
./docker-run.sh reproduce

# Run only the analysis (faster, skips some setup)
./docker-run.sh analysis

# Start Jupyter Lab for interactive analysis
./docker-run.sh jupyter

# Open an interactive shell in the container
./docker-run.sh shell

# Clean up Docker images and containers
./docker-run.sh clean
```

### Direct Docker Commands

You can also use Docker directly:

```bash
# Build the image
docker build -t beyond-the-streetlight .

# Run the reproduction
docker run --rm -v $(pwd)/results:/app/results -v $(pwd)/figures:/app/figures beyond-the-streetlight

# Run with Docker Compose
docker-compose run --rm reproduce
```

### Docker Benefits

- **Complete Isolation**: No conflicts with your local Python environment
- **Reproducibility**: Identical environment across all machines
- **Easy Setup**: No need to install Python, Poetry, or dependencies locally
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Version Control**: Docker image captures the exact software environment
