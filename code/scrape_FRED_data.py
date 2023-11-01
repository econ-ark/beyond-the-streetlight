import pandas as pd
import requests
import xml.etree.ElementTree as ET

# Replace with your FRED API key
api_key = "YOUR_API_KEY"

# Define the series IDs and their respective frequencies
series_data = [
    {"id": "UNRATE", "name": "Civilian Unemployment Rate", "frequency": "q"},
    {"id": "PCEPI", "name": "Headline PCE Inflation Rate", "frequency": "m"},
    {"id": "PCEPILFE", "name": "Core PCE Inflation Rate", "frequency": "m"},
    {"id": "DPCERL1Q225SBEA", "name": "Real Personal Consumption Expenditures", "frequency": "m"},
]

# Define the date range
start_date = "2006-01-01"
end_date = pd.Timestamp.now().strftime("%Y-%m-%d")

# Initialize a dictionary to store the data
data = {}

# Loop through the series data
for series in series_data:
    params = {
        "series_id": series["id"],
        "api_key": api_key,
        "file_type": "xml",
        "observation_start": start_date,
        "observation_end": end_date,
    }

    # Specify the frequency parameter
    if series["frequency"] == "q":
        params["frequency"] = "q"

    response = requests.get("https://api.stlouisfed.org/fred/series/observations", params=params)

    if response.status_code == 200:
        root = ET.fromstring(response.text)
        observations = root.find(".//observations")
        data[series["name"]] = {point.find('date').text: point.find('value').text for point in observations}
    else:
        print(f"Failed to fetch data for {series['name']}")

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Print the first few rows of the DataFrame
print(df)

