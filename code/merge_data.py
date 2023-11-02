import pandas as pd
import numpy as np

GB = pd.read_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/GB.csv')
SPF = pd.read_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/SPF.csv')
FRED = pd.read_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/FRED.csv')

# Add NaN values to SPF and GB for the dates before 2007 Q1 where there is FRED data for
nan_rows_GB = pd.DataFrame(np.nan, index=np.arange(FRED.shape[0] - GB.shape[0]), columns=GB.columns)
GB = pd.concat([nan_rows_GB, GB], ignore_index=True)

nan_rows_SPF = pd.DataFrame(np.nan, index=np.arange(FRED.shape[0] - SPF.shape[0]), columns=SPF.columns)
SPF = pd.concat([nan_rows_SPF, SPF], ignore_index=True)

# Remove the first two columns of GB and SPF that capture dates and indexing
GB = GB.iloc[:, 2:]
SPF = SPF.iloc[:, 2:]

merged_df = pd.concat([FRED, GB, SPF], axis=1)

print(merged_df)

merged_df.to_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/merged.csv')
