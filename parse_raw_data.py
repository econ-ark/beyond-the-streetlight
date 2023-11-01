import pandas as pd

# Load the Excel file
excel_file = pd.ExcelFile('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/GBweb_Row_Format.xlsx') 

# First for unemployment
df = excel_file.parse('UNEMP')
date_1 = df['DATE']
unemp_f = df['UNEMPF4']

# Then for both inflation measures
df = excel_file.parse('gPPCE')
date_2 = df['DATE']
headline_f = df['gPPCEF4']

df = excel_file.parse('gPPCEX')
date_3 = df['DATE']
core_f = df['gPPCEXF4']

# Lastly for real expenditures
df = excel_file.parse('gRPCE')
date_4 = df['DATE']
cons_f = df['gRPCEF4']

# Store them all in a single frame
result_df = pd.DataFrame({'DATE1': date_1, 'UNEMPF4': unemp_f,
                          'DATE2': date_2, 'gPPCEF4': headline_f,
                          'DATE3': date_3, 'gPPCEXF4': core_f,
                          'DATE4': date_4, 'gRPCEF4': cons_f})

# Print the final result
print(result_df)

result_df.to_excel('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/GBweb_parsed.xlsx', index=False)
