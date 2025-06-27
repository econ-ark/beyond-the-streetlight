#!/bin/bash

# Full reproduction script for REMARK compliance
# This script supports both Poetry and conda environments

echo "🔄 Starting full reproduction workflow..."

# Get the script directory
SCPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
cd "$SCPT_DIR"

# Record start time
start_time=$(date +%s)

# Determine which environment manager to use
USE_POETRY=false
USE_CONDA=false

# Check if we're in a conda environment
if [[ -n "$CONDA_DEFAULT_ENV" ]]; then
    echo "✅ Detected conda environment: $CONDA_DEFAULT_ENV"
    USE_CONDA=true
elif command -v conda &> /dev/null && [ -f "binder/environment.yml" ]; then
    echo "🐍 Conda available and binder/environment.yml found"
    echo "💡 Consider activating the conda environment:"
    echo "   conda env create -f binder/environment.yml"
    echo "   conda activate rs100_discussion"
    USE_CONDA=true
fi

# Check if Poetry is available
if command -v poetry &> /dev/null && [ -f "pyproject.toml" ]; then
    echo "📝 Poetry available and pyproject.toml found"
    USE_POETRY=true
fi

# Determine execution method
if [[ "$USE_CONDA" == true && -n "$CONDA_DEFAULT_ENV" ]]; then
    echo "🚀 Using conda environment for execution"
    PYTHON_CMD="python"
    
    # Check for required packages
    echo "🔍 Checking Python dependencies..."
    python -c "import pandas, numpy, matplotlib, fredapi, statsmodels" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "❌ Required Python packages not found in conda environment."
        echo "💡 Please ensure conda environment is properly set up:"
        echo "   conda env create -f binder/environment.yml"
        echo "   conda activate rs100_discussion"
        exit 1
    fi
    
elif [[ "$USE_POETRY" == true ]]; then
    echo "🚀 Using Poetry for execution"
    
    # Install dependencies using Poetry
    echo "📦 Installing dependencies with Poetry..."
    poetry install
    
    # Check if installation was successful
    if [ $? -ne 0 ]; then
        echo "❌ Poetry install failed. Please check the error messages above."
        exit 1
    fi
    
    PYTHON_CMD="poetry run python"
    
else
    echo "❌ Neither conda environment nor Poetry is properly configured."
    echo "💡 Please either:"
    echo "   1. Set up conda environment: conda env create -f binder/environment.yml && conda activate rs100_discussion"
    echo "   2. Install Poetry and run: poetry install"
    exit 1
fi

echo "🎯 Running reproduction workflow..."

# Execute the Jupyter notebook if available
echo "📓 Processing Jupyter notebook..."
if ls *.ipynb 1> /dev/null 2>&1; then
    echo "ℹ️  Found Jupyter notebooks, attempting to execute..."
    
    if [[ "$USE_CONDA" == true && -n "$CONDA_DEFAULT_ENV" ]]; then
        # Use conda environment
        if python -c "import jupyter" 2>/dev/null; then
            python -m jupyter nbconvert --to notebook --execute --inplace *.ipynb
        elif python -c "import nbconvert" 2>/dev/null; then
            python -m nbconvert --to notebook --execute --inplace *.ipynb  
        else
            echo "⚠️  Jupyter/nbconvert not available, skipping notebook execution."
        fi
    else
        # Use Poetry
        if poetry run python -c "import jupyter" 2>/dev/null; then
            poetry run python -m jupyter nbconvert --to notebook --execute --inplace *.ipynb
        elif poetry run python -c "import nbconvert" 2>/dev/null; then
            poetry run python -m nbconvert --to notebook --execute --inplace *.ipynb  
        else
            echo "⚠️  Jupyter/nbconvert not available, skipping notebook execution."
        fi
    fi
    echo "✅ Notebook processing completed."
else
    echo "ℹ️  No Jupyter notebooks found, skipping notebook execution."
fi

# Run the main reproduction script
echo "🚀 Running main analysis scripts..."
$PYTHON_CMD code/main/reproduce.py

# Check if analysis was successful
if [ $? -ne 0 ]; then
    echo "❌ Main analysis execution failed."
    exit 1
fi

# Calculate and display runtime
end_time=$(date +%s)
runtime=$((end_time - start_time))
echo "🎉 Full reproduction completed successfully!"
echo "⏱️  Total runtime: ${runtime} seconds"

# Verify key output files exist
echo "✅ Verifying output files..."
expected_files=(
    "data/output/GB.csv"
    "data/output/SPF.csv" 
    "data/output/FRED.csv"
    "data/output/forecast.csv"
    "data/output/errors.csv"
    "data/output/abs_errors.csv"
)

missing_files=()
for file in "${expected_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -eq 0 ]; then
    echo "✅ All expected output files generated successfully."
else
    echo "⚠️  Warning: Missing output files:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
fi

echo ""
echo "📊 Reproduction workflow completed!"
echo "📝 For faster testing, you can also use: ./reproduce_min.sh"



