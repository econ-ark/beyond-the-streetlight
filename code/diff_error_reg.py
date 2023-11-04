import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.stats.stattools import durbin_watson

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
diff_sqe_columns = ["Diff_SqE_unemp","Diff_SqE_rPCE"]

# Extract year and quarter as separate variables
data['Year'] = data['date'].dt.year

# Create a 1x2 grid of plots
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Loop through the squared error columns
for i, squared_error_column in enumerate(diff_sqe_columns):
    model = sm.OLS(data[squared_error_column], data[['Constant', 'Year']])
    results = model.fit(cov_type="HC3")

    print(f"Regression Summary for {squared_error_column}:")
    print(results.summary())
    print("\n")

    # Calculate the residuals
    residuals = results.resid

    # Compute the Mean Squared Error (MSE)
    mse = (residuals ** 2).mean()
    print(f"Mean Squared Error for {squared_error_column}: {mse:.4f}")

    # Perform the Durbin-Watson test
    durbin_watson_statistic = durbin_watson(residuals)
    print(f"Durbin-Watson Statistic for {squared_error_column}: {durbin_watson_statistic}")

    # Predict values based on the regression model
    predicted_values = results.predict(data[['Constant', 'Year']])

    # Plot the predicted values with time on the x-axis in the corresponding subplot
    ax = axes[i]
    ax.plot(data['Year'], predicted_values, label=f'Predicted {squared_error_column}')
    ax.plot(data['Year'], data[squared_error_column], label=f'Actual {squared_error_column}', linestyle='--', color="black")
    ax.set_xlabel("Year")
    ax.set_ylabel("Values")
    ax.set_title(f"{squared_error_column} Over Time")
    ax.legend()

# Ensure proper spacing between subplots
plt.tight_layout()
save_path = "/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/figures/diff_SqE_reg.png" 
plt.savefig(save_path, format='png')
plt.show()





