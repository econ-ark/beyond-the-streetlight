import pandas as pd

# Load the Excel file with levels first
excel_file = pd.ExcelFile('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/meanLevel.xlsx') 

# Extract unemployment; starting from 2007 Q1 so that there are forecasts for every variable
df = excel_file.parse('UNEMP')
date = df['YEAR'][153:197]  
unemp_f = df['UNEMP4'][153:197]  

# Then for both inflation measures
df = excel_file.parse('PCE')
headline_f = df['PCE4'][153:197]  

df = excel_file.parse('COREPCE')
core_f = df['COREPCE4'][153:197]  

# Lastly, load the Excel file with growth in level and extract data for real expenditures
excel_file = pd.ExcelFile('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/meanGrowth.xlsx') 
df = excel_file.parse('RCONSUM')
cons_f = df['drconsum4'][153:197]  

# Create DataFrames for each data source
date_df = pd.DataFrame({'DATE': date}).reset_index(drop=True)
unemp_df = pd.DataFrame({'SPF_UNEMPF2': unemp_f}).reset_index(drop=True)
headline_df = pd.DataFrame({'SPF_INFF2': headline_f}).reset_index(drop=True)
core_df = pd.DataFrame({'SPF_COREINFF2': core_f}).reset_index(drop=True)
cons_df = pd.DataFrame({'SPF_gRPCEF2': cons_f}).reset_index(drop=True)

# Concatenate the DataFrames to create result_df
result_df = pd.concat([date_df, unemp_df, headline_df, core_df, cons_df], axis=1)

# Print the final result
print(result_df)

df.to_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/SPF.csv')
#result_df.to_excel('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/SPFweb_parsed.xlsx', index=False)