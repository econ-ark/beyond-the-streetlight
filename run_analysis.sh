#!/bin/bash

# Analysis execution script
# This script contains the core analysis workflow and can be called by:
# 1. reproduce.sh (after dependency installation)
# 2. CI/CD pipelines (assuming dependencies are already installed)

echo "Starting analysis workflow..."

# Get the script directory
SCPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
cd "$SCPT_DIR"

# Record start time
start_time=$(date +%s)

# Run the Jupyter notebook
echo "Executing Jupyter notebook..."
if ls *.ipynb 1> /dev/null 2>&1; then
    echo "ℹ️  Found Jupyter notebooks, attempting to execute..."
    # Try different methods to execute the notebook
    if poetry run python -c "import jupyter"; then
        poetry run python -m jupyter nbconvert --to notebook --execute --inplace *.ipynb
    elif poetry run python -c "import nbconvert"; then
        poetry run python -m nbconvert --to notebook --execute --inplace *.ipynb  
    else
        echo "⚠️  Jupyter/nbconvert not available, skipping notebook execution."
        echo "   This may affect some results, but main analysis will continue."
    fi
    echo "✅ Notebook processing completed."
else
    echo "ℹ️  No Jupyter notebooks found, skipping notebook execution."
fi

# Run the main reproduction script
echo "Running main analysis scripts..."
poetry run python code/main/reproduce.py

# Check if analysis was successful
if [ $? -ne 0 ]; then
    echo "❌ Main analysis execution failed."
    exit 1
fi

# Calculate and display runtime
end_time=$(date +%s)
runtime=$((end_time - start_time))
echo "✅ Analysis workflow completed successfully!"
echo "📊 Total analysis runtime: ${runtime} seconds"

# Optional: Verify key output files exist
echo "Verifying output files..."
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