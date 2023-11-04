import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.stats.stattools import durbin_watson
import os

errors = pd.read_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/errors.csv')

# Convert the "date" column to datetime if not already in datetime format
errors['date'] = pd.to_datetime(errors['date'])
sample_size = 0 # set to 48 if you want to start with year 1995 Q1
ss_q = int(sample_size/4)

# Now retain only the annual forecasts/actual changes and the date column
data = errors.iloc[sample_size:, [1] + list(range(-6, 0))] 

# Create a constant term for the regression
data['Constant'] = 1

# List of squared error column names to perform regressions on
diff_sqe_cols = ["diff_error_unemp","diff_error_cons"]

# Extract year and quarter as separate variables
data['Year'] = data['date'].dt.year

# Create a 1x2 grid of plots
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
output_dir = '/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/results'
summary_text = ""

# Loop through the squared error columns
for i, diff_sqe_col in enumerate(diff_sqe_cols):
    model = sm.OLS(data[diff_sqe_col], data[['Constant', 'Year']])
    results = model.fit(cov_type="HC3")

    print(f"Regression Summary for {diff_sqe_col}:")
    print(results.summary())
    print("\n")

    summary_text += f"Regression Summary for {diff_sqe_col}:\n"
    summary_text += results.summary().as_text() + "\n"

    # Calculate the residuals
    residuals = results.resid

    # Compute the Mean Squared Error (MSE)
    mse = (residuals ** 2).mean()
    print(f"Mean Squared Error for {diff_sqe_col}: {mse:.4f}")
    summary_text += f"Mean Squared Error for {diff_sqe_col}: {mse:.4f}\n"

    # Perform the Durbin-Watson test
    durbin_watson_statistic = durbin_watson(residuals)
    print(f"Durbin-Watson Statistic for {diff_sqe_col}: {durbin_watson_statistic}")
    summary_text += f"Durbin-Watson Statistic for {diff_sqe_col}: {durbin_watson_statistic}\n"

    # Predict values based on the regression model
    predicted_values = results.predict(data[['Constant', 'Year']])

    # Plot the predicted values with time on the x-axis in the corresponding subplot
    ax = axes[i]
    ax.plot(data['Year'], predicted_values, label=f'Predicted {diff_sqe_col}')
    ax.plot(data['Year'], data[diff_sqe_col], label=f'Actual {diff_sqe_col}', linestyle='--', color="black")
    ax.set_xlabel("Year")
    ax.set_ylabel("Values")
    ax.set_title(f"{diff_sqe_col} Over Time")
    ax.legend()

# Save all regression summaries to a single text file
summary_file_path = os.path.join(output_dir, f"diff_sqe_reg_{1983+ss_q}.txt")
with open(summary_file_path, 'w') as summary_file:
    summary_file.write(summary_text)

# Ensure proper spacing between subplots
plt.tight_layout()
if ss_q == 0:
    save_path = "/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/figures/diff_sqe_reg_1983.png" 
else:
    save_path = "/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/figures/diff_sqe_reg_1995.png"
plt.savefig(save_path, format='png')
plt.show()





