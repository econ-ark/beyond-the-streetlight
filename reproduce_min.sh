#!/bin/bash

# Minimal reproduction script for REMARK compliance
# This script works with the conda environment specified in binder/environment.yml
# and provides a faster execution path for testing

echo "🔄 Starting minimal reproduction workflow..."

# Get the script directory
SCPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
cd "$SCPT_DIR"

# Record start time
start_time=$(date +%s)

# Check if we're in a conda environment
if [[ -n "$CONDA_DEFAULT_ENV" ]]; then
    echo "✅ Running in conda environment: $CONDA_DEFAULT_ENV"
else
    echo "⚠️  No conda environment detected. Proceeding with system Python."
fi

# Check for required Python packages
echo "🔍 Checking Python dependencies..."
python -c "import pandas, numpy, matplotlib, fredapi, statsmodels" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Required Python packages not found."
    echo "💡 Please ensure you're running in the conda environment:"
    echo "   conda env create -f binder/environment.yml"
    echo "   conda activate rs100_discussion"
    exit 1
fi

# Run core analysis (skip notebook execution for speed)
echo "🚀 Running core analysis scripts..."
python code/main/reproduce.py

# Check if analysis was successful
if [ $? -ne 0 ]; then
    echo "❌ Core analysis execution failed."
    exit 1
fi

# Verify key output files exist
echo "✅ Verifying essential output files..."
essential_files=(
    "data/output/GB.csv"
    "data/output/SPF.csv" 
    "data/output/FRED.csv"
)

missing_files=()
for file in "${essential_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -eq 0 ]; then
    echo "✅ Essential output files generated successfully."
else
    echo "❌ Missing essential output files:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    exit 1
fi

# Calculate and display runtime
end_time=$(date +%s)
runtime=$((end_time - start_time))
echo "🎉 Minimal reproduction completed successfully!"
echo "⏱️  Runtime: ${runtime} seconds"
echo ""
echo "📝 Note: This is the minimal reproduction script."
echo "   For full reproduction including notebook execution, use: ./reproduce.sh" 