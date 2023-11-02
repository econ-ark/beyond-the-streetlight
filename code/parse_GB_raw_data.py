import pandas as pd

# Load the Excel file
excel_file = pd.ExcelFile('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/raw/GBweb_Row_Format.xlsx') 

# First for unemployment; note, we want from 2007, Q1 onward to align with SPF data
df = excel_file.parse('UNEMP')
date = df['DATE'][378:]
unemp_f = df['UNEMPF2'][378:]

# Then for both inflation measures
df = excel_file.parse('gPPCE')
headline_f = df['gPPCEF2'][56:]

df = excel_file.parse('gPPCEX')
core_f = df['gPPCEXF2'][56:]

# Lastly for real expenditures
df = excel_file.parse('gRPCE')
cons_f = df['gRPCEF2'][235:]

# Create DataFrames for each data source and reset the index
date_df = pd.DataFrame({'DATE': date}).reset_index(drop=True)
unemp_df = pd.DataFrame({'GB_UNEMPF2': unemp_f}).reset_index(drop=True)
headline_df = pd.DataFrame({'GB_INFF2': headline_f}).reset_index(drop=True)
core_df = pd.DataFrame({'GB_COREINFF2': core_f}).reset_index(drop=True)
cons_df = pd.DataFrame({'GB_gRPCEF2': cons_f}).reset_index(drop=True)

# Concatenate the DataFrames to ensure correct alignment
result_df = pd.concat([date_df, unemp_df, headline_df, core_df, cons_df], axis=1)

# Print the final result
print(result_df)

# Now, since Greenbook has two forecast per quarter, we extract the final forecast for a given
# quarter, since this gives us the best chance at getting the FED's forecast *after* the SPF
# forecast is made.

# Extract odd-numbered rows (1, 3, ..., 43)
GB_df = result_df.iloc[1::2]

# Reset the index for the modified DataFrame
GB_df.reset_index(drop=True, inplace=True)

# Continue working with the 'odd_rows_df' DataFrame
print(GB_df)

# Uncomment these final lines to get the output of your choice
GB_df.to_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/GB.csv')
# GB_df.to_excel('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/GB_parsed.xlsx', index=False)
