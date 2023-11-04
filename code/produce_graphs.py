import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def graph(df, x_column, y_columns, title):
    """
    Function which produces graphs capturing the forecast errors of the 
    GB and SPF for a number of variables.

    Be sure to put the variables in the following order: Actual, GB, SPF. This
    way the labels will align properly
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_column], df[y_columns[0]], label="Actual", linestyle="-", color="black")
    plt.plot(df[x_column], df[y_columns[1]], label="GB", linestyle="--", color="red")
    plt.plot(df[x_column], df[y_columns[2]], label="SPF", linestyle="--", color="blue")
    plt.xlabel("Time")
    plt.ylabel("Annual change")
    plt.title(title)
    plt.legend()
    plt.grid(True)

    # Set the x-axis limits
    plt.xlim(df[x_column].iloc[0], df[x_column].iloc[-1])

    # Use date locator and formatter for x-axis
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(base=3))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    #plt.show()

# Now retrieve the dataframe to produce graphs
forecast = pd.read_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/forecast.csv')

# Convert the "date" column to datetime if not already in datetime format
forecast['date'] = pd.to_datetime(forecast['date'])

# Now retain only the annual forecasts/actual changes and the date column
data = forecast.iloc[:, [1] + list(range(-12,0))]

# 1. Unemployment 
x_column = "date"  
y_columns = ["YoY_Unemp", "YoY_Unemp_GB", "YoY_Unemp_SPF"]

graph(data, x_column, y_columns, "Unemployment forecasts vs data")
save_path = "/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/figures/unemp_forecast.png" 
plt.savefig(save_path, format='png')
plt.show()

# 2. Growth in real PCE 
x_column = "date"  
y_columns = ["YoY_rPCE", "YoY_rPCE_GB", "YoY_rPCE_SPF"]

graph(data, x_column, y_columns, "Real consumption growth forecasts vs data")
save_path = "/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/figures/cons_forecast.png" 
plt.savefig(save_path, format='png')
plt.show()
