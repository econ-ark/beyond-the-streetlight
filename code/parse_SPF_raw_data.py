import pandas as pd

# Load the Excel file with levels first
excel_file = pd.ExcelFile('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/raw/meanLevel.xlsx') 

# Extract unemployment; starting from 2007 Q1 so that there are forecasts for every variable
df = excel_file.parse('UNEMP')
date = df['YEAR'][53:197]  
unemp_f = df['UNEMP4'][53:197]  
 

# Lastly, load the Excel file with growth in level and extract data for real expenditures
excel_file = pd.ExcelFile('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/raw/meanGrowth.xlsx') 
df = excel_file.parse('RCONSUM')
cons_f = df['drconsum4'][53:197]  

# Create DataFrames for each data source
date_df = pd.DataFrame({'DATE': date}).reset_index(drop=True)
unemp_df = pd.DataFrame({'SPF_UNEMPF2': unemp_f}).reset_index(drop=True)
cons_df = pd.DataFrame({'SPF_gRPCEF2': cons_f}).reset_index(drop=True)

# Concatenate the DataFrames to create result_df
SPF_df = pd.concat([date_df, unemp_df, cons_df], axis=1)

# Print the final result
print(SPF_df)

# Uncomment these final lines to get the output of your choice
SPF_df.to_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/SPF.csv')
# SPF_df.to_excel('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/SPF_parsed.xlsx', index=False)