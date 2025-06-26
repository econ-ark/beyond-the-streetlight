# AI Repository Description: Beyond the Streetlight

## Repository Overview
**Purpose**: Analysis of forecast error trends in Federal Reserve Tealbook/Greenbook and Survey of Professional Forecasters data from 1982-2017

**Research Type**: REMARK (Replication/Exploration) - Computational economics research with full reproducibility

**Academic Context**: Centennial celebration of Federal Reserve Research & Statistics Division, examining evolution of economic measurement and forecasting accuracy

## Core Research Questions
1. How have forecast errors evolved over time for unemployment and consumption forecasts?
2. What are the differences in forecast accuracy between Fed internal forecasts vs. professional forecasters?
3. How do forecast errors relate to broader economic measurement challenges?

## Data Sources and Variables
### Primary Data
- **Tealbook/Greenbook Forecasts**: Federal Reserve internal economic forecasts
  - Variables: Unemployment rate, Real PCE growth
  - Source: Philadelphia Fed
  - Time period: 1982-2017
  
- **Survey of Professional Forecasters**: Private sector economic forecasts
  - Variables: Same as Tealbook/Greenbook
  - Source: Philadelphia Fed
  - Coverage: Mean across private forecasters

- **Realized Values**: Actual economic outcomes
  - Source: Federal Reserve Economic Data (FRED)
  - Used for forecast error calculation

### Derived Variables
- Absolute forecast errors (ABS_ERROR)
- Squared forecast errors (SQE)
- Forecast horizons (multiple periods ahead)
- Cross-sectional differences between forecasters

## Methodology and Techniques
### Statistical Methods
- **Error Decomposition**: Breaking down forecast errors by source and horizon
- **Regression Analysis**: Examining trends in forecast accuracy over time
- **Comparative Analysis**: Fed vs. private forecaster performance

### Computational Approach
- **Python**: Primary programming language
- **Pandas**: Data manipulation and analysis
- **Matplotlib/Seaborn**: Visualization
- **Statsmodels**: Statistical modeling
- **Jupyter Notebooks**: Interactive analysis and presentation

### Reproducibility Features
- Complete data pipeline from raw sources to final results
- Automated data retrieval from FRED API
- Version-controlled analysis scripts
- Binder-compatible environment for cloud execution

## Key Findings and Contributions
### Empirical Results
- Trends in forecast accuracy over 35-year period
- Relative performance of different forecasting approaches
- Insights into economic measurement challenges

### Methodological Contributions
- Replicable framework for forecast evaluation
- Integration of multiple forecasting data sources
- Template for longitudinal forecast accuracy studies

## Technical Implementation
### File Structure
```
beyond-the-streetlight/
├── code/
│   ├── main/           # Core analysis scripts
│   │   ├── scrape_FRED_data.py
│   │   ├── parse_GB_raw_data.py
│   │   ├── parse_SPF_raw_data.py
│   │   ├── compute_abs_error.py
│   │   └── reproduce.py
│   └── other/          # Additional analysis
├── data/
│   ├── raw/           # Original data files
│   └── output/        # Processed datasets
├── figures/           # Generated visualizations
├── results/           # Statistical output
└── RS100_Discussion_Slides.ipynb  # Main presentation
```

### Environment Requirements
- Python 3.8+
- Scientific Python stack (NumPy, Pandas, Matplotlib)
- Statistical libraries (Statsmodels, SciPy)
- Data access tools (FRED API, web scraping)

## Integration with Broader Research
### Related Literature
- Economic forecasting accuracy studies
- Central bank communication research
- History of economic measurement

### Policy Relevance
- Federal Reserve forecasting processes
- Economic policy decision-making under uncertainty
- Evolution of macroeconomic modeling

### Academic Impact
- Demonstrates reproducible research practices
- Provides template for forecast evaluation studies
- Contributes to literature on economic measurement

## Usage and Applications
### Educational Use
- Graduate courses in macroeconomics
- Econometrics methodology classes
- Research methods in economics

### Research Extensions
- Additional forecast variables (inflation, GDP growth)
- International comparisons of forecast accuracy
- Integration with economic policy analysis

### Policy Applications
- Central bank forecasting evaluation
- Economic policy communication strategies
- Historical analysis of economic measurement

## Technical Keywords
**Primary**: forecast accuracy, economic measurement, Federal Reserve, reproducible research
**Secondary**: Tealbook, Greenbook, Survey of Professional Forecasters, unemployment forecasting, consumption forecasting
**Methodological**: Python, Jupyter notebooks, time series analysis, forecast evaluation, data visualization
**Academic**: computational economics, empirical macroeconomics, central banking, economic history

## Citation and Attribution
**Authors**: Decory Edwards, Christopher Carroll
**Institution**: Johns Hopkins University, Econ-ARK
**Event**: Federal Reserve R&S Centennial Conference (2023)
**Repository**: https://github.com/dedwar65/beyond-the-streetlight
**License**: Apache 2.0

## Reproducibility Statement
This repository adheres to REMARK standards for computational reproducibility:
- ✅ Tagged release (v1.0.4)
- ✅ Complete reproduction script (`reproduce.sh`)
- ✅ Environment specification (`binder/environment.yml`)
- ✅ Bibliographic metadata (`CITATION.cff`)
- ✅ Cloud execution via MyBinder

**Execution Time**: Approximately 10-15 minutes on standard hardware
**Cloud Access**: Available via MyBinder at repository link
**Data Dependencies**: Automatic download from public sources (FRED, Philadelphia Fed)

---

*This description is optimized for AI discovery and academic indexing. Repository status: Active, maintained, fully reproducible.* 