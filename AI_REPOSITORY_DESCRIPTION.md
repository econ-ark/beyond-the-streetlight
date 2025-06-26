# Beyond the Streetlight: AI-Friendly Repository Description

## Repository Overview

**Repository Name**: Beyond the Streetlight  
**Type**: Economic Research Reproduction and Analysis  
**Domain**: Macroeconomic Forecasting, Federal Reserve Economics  
**Programming Language**: Python  
**License**: Open Source  
**Reproducibility Standard**: REMARK (Replications and Explorations Made Available to Everyone)

## Research Purpose and Questions

This repository contains a comprehensive econometric analysis that addresses the following research questions:

1. **Primary Research Question**: How have the accuracy of economic forecasts evolved over time?
2. **Specific Focus**: Analysis of forecast error trends in unemployment rate and real personal consumption expenditure growth predictions from 1982-2017
3. **Comparative Analysis**: Evaluation of forecast accuracy between two major forecasting sources:
   - Federal Reserve's Tealbook/Greenbook (GB) - official central bank forecasts
   - Survey of Professional Forecasters (SPF) - consensus of private sector economists

## Methodology and Analysis Framework

### Data Sources
1. **Federal Reserve Forecasts (Greenbook/Tealbook)**:
   - Source: Philadelphia Federal Reserve Bank
   - URL: https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/philadelphia-data-set
   - Contains official Federal Reserve economic projections

2. **Survey of Professional Forecasters (SPF)**:
   - Source: Philadelphia Federal Reserve Bank  
   - URL: https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/mean-forecasts
   - Contains consensus forecasts from private sector economists

3. **Realized Economic Data**:
   - Source: Federal Reserve Economic Data (FRED), St. Louis Fed
   - URL: https://fred.stlouisfed.org/
   - Contains actual observed values for comparison with forecasts

### Statistical Methods
- **Absolute Error Analysis**: Computation of absolute forecast errors
- **Time Series Regression**: OLS regression with heteroscedasticity-robust standard errors (HC3)
- **Trend Analysis**: Evaluation of forecast accuracy improvement over time
- **Comparative Statistical Testing**: Durbin-Watson statistics for autocorrelation analysis

### Variables Analyzed
1. **Unemployment Rate Forecasts**:
   - 4-quarter ahead forecasts (UNEMPF4)
   - Current quarter nowcasts (UNEMPF0)

2. **Real Personal Consumption Expenditure Growth**:
   - Multi-horizon forecasts (gRPCEF0, gRPCEF1, gRPCEF2, gRPCEF3)
   - Annual growth rate calculations

## Key Findings and Results

### Quantitative Results
1. **Forecast Accuracy Levels** (Mean Absolute Errors):
   - GB Unemployment Errors: 0.526 percentage points
   - SPF Unemployment Errors: 0.538 percentage points
   - GB Consumption Errors: 1.022 percentage points
   - SPF Consumption Errors: 1.096 percentage points

2. **Trend Analysis**:
   - **Consumption Forecasts**: Statistically significant improvement over time
     - GB: R-squared = 0.219, coefficient = -0.0393 (p < 0.001)
     - SPF: R-squared = 0.133, coefficient = -0.0314 (p < 0.001)
   - **Unemployment Forecasts**: No significant trend improvement
     - GB: R-squared = 0.013, coefficient = -0.0061 (p = 0.185)
     - SPF: R-squared = 0.005, coefficient = -0.0038 (p = 0.413)

### Economic Significance
- **Federal Reserve forecasts** show slightly better performance than private sector consensus
- **Consumption growth forecasts** have improved significantly over the 35-year period
- **Unemployment forecasts** show no systematic improvement, suggesting inherent forecasting challenges

## Technical Implementation

### Programming Environment
- **Language**: Python 3.9+
- **Dependency Management**: Poetry (pyproject.toml)
- **Key Libraries**:
  - pandas (2.1.3+): Data manipulation and analysis
  - numpy (1.26.0+): Numerical computations
  - statsmodels (0.14.0+): Econometric analysis
  - matplotlib (3.8.1+): Data visualization
  - fredapi (0.4.2+): Federal Reserve data access
  - fredpy (3.2.8+): FRED data processing
  - openpyxl (3.1.2+): Excel file processing

### Data Pipeline Architecture
```
Raw Data → Data Parsing → FRED API Integration → Forecast Computation → Error Analysis → Statistical Modeling → Results Output
```

### File Structure and Components

#### Core Analysis Scripts (`code/main/`)
1. **parse_GB_raw_data.py**: Processes Federal Reserve Greenbook/Tealbook forecast data
2. **parse_SPF_raw_data.py**: Processes Survey of Professional Forecasters data
3. **scrape_FRED_data.py**: Downloads realized economic data from FRED API
4. **annual_forecasts.py**: Computes annual forecast horizons from quarterly data
5. **compute_abs_error.py**: Calculates absolute forecast errors and summary statistics
6. **abse_reg.py**: Performs regression analysis of forecast error trends

#### Data Organization (`data/`)
- **raw/**: Original data files (Excel format)
  - GBweb_Row_Format.xlsx: Greenbook forecasts
  - meanGrowth.xlsx, meanLevel.xlsx: SPF forecasts
- **output/**: Processed datasets (CSV format)
  - GB.csv, SPF.csv: Parsed forecast data
  - FRED.csv: Realized values
  - forecast.csv: Combined forecast dataset
  - errors.csv, abs_errors.csv: Error calculations

#### Results and Outputs (`results/`, `figures/`)
- **Statistical Results**: Text files with regression outputs
- **Visualizations**: PNG format charts showing forecast performance
- **Comparative Analysis**: Difference plots between forecasting sources

### Reproducibility Features
1. **Automated Setup**: `install.sh` script for dependency installation
2. **One-Click Reproduction**: `reproduce.sh` script runs entire analysis pipeline
3. **Containerization**: Poetry virtual environment ensures consistent execution
4. **Comprehensive Documentation**: README.md with setup and usage instructions

## Research Context and Significance

### Academic Contribution
- **Field**: Macroeconomic Forecasting, Central Banking, Applied Econometrics
- **Time Period**: 35-year longitudinal study (1982-2017)
- **Policy Relevance**: Evaluation of Federal Reserve forecasting capability
- **Methodological Innovation**: Comparative analysis of institutional vs. consensus forecasts

### Related Research Areas
- Central bank communication and transparency
- Professional forecaster behavior and incentives
- Macroeconomic forecast evaluation methodologies
- Real-time data analysis in monetary policy

### Data Vintage and Coverage
- **Temporal Scope**: 1982 Q1 - 2017 Q4 (144 quarterly observations)
- **Variable Coverage**: Core macroeconomic indicators (unemployment, consumption)
- **Forecast Horizons**: Current quarter through 3-quarters ahead
- **Data Frequency**: Quarterly observations with annual aggregation

## Usage and Access Information

### Prerequisites
- Python 3.9 or higher
- Internet connection (for FRED data access)
- 50MB disk space for data and results

### Installation Commands
```bash
# Automatic setup
./install.sh

# Manual setup
poetry install
```

### Execution Commands
```bash
# Full reproduction workflow
./reproduce.sh

# Individual script execution
poetry run python code/main/reproduce.py
```

### Expected Runtime
- **Total Analysis Time**: ~15-30 seconds
- **Data Download**: ~5-10 seconds (FRED API calls)
- **Computation**: ~10-20 seconds (regression analysis)

## Output Artifacts

### Statistical Results
- Regression coefficients with standard errors
- R-squared and F-statistics
- Durbin-Watson test statistics
- Mean squared error calculations

### Visualizations
- Time series plots of forecast errors
- Regression trend lines
- Comparative accuracy charts
- Difference plots between forecasting sources

### Data Products
- Cleaned and merged datasets
- Forecast error time series
- Annual aggregated forecasts
- Combined GB-SPF-FRED dataset

This repository serves as a comprehensive resource for understanding the evolution of macroeconomic forecasting accuracy and provides a fully reproducible research pipeline for economic forecast evaluation. 