import pandas as pd
import statsmodels.api as sm

# Load your data (assuming you have a DataFrame with columns "Time" and "Squared_Errors")
# You may need to modify this based on your actual data structure
forecast = pd.read_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/forecast.csv')

# Convert the "date" column to datetime if not already in datetime format
forecast['date'] = pd.to_datetime(forecast['date'])

# Now retain only the annual forecasts/actual changes and the date column
data = forecast.iloc[4:, [1] + list(range(-4,0))]
print(data)


# Create a constant term for the regression
data['Constant'] = 1

# List of squared error column names to perform regressions on
squared_error_columns = ['MSE_Unemp(GB)', 'MSE_rPCE(GB)', 'MSE_unemp(SPF)',"MSE_rPCE(SPF)"]

# Extract year and quarter as separate variables
data['Year'] = data['date'].dt.year
data['Quarter'] = data['date'].dt.quarter

# Perform regressions for each squared error column
for squared_error_column in squared_error_columns:
    model = sm.OLS(data[squared_error_column], data[['Constant', 'Year', 'Quarter']])
    results = model.fit()

    # Print the regression summary for each squared error column
    print(f"Regression Summary for {squared_error_column}:")
    print(results.summary())
    print("\n")





