import pandas as pd
import numpy as np

GB = pd.read_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/GB.csv')
SPF = pd.read_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/SPF.csv')
FRED = pd.read_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/FRED.csv')

#Remove the first two columns of GB and SPF that capture dates and indexing
GB = GB.iloc[:, 2:]
SPF = SPF.iloc[:, 2:]

# Remove the first two rows of FRED
FRED = FRED.iloc[2:]

# Add two rows of NaN values to the top of GB and SPF
nan_rows_top = pd.DataFrame(np.nan, index=np.arange(2), columns=GB.columns)
GB = pd.concat([nan_rows_top, GB], ignore_index=True)
SPF = pd.concat([nan_rows_top, SPF], ignore_index=True)

# Reset the index of the individual dataframes
GB = GB.reset_index(drop=True)
SPF = SPF.reset_index(drop=True)
FRED = FRED.reset_index(drop=True)

merged_df = pd.concat([FRED, GB, SPF], axis=1)
print(merged_df.shape)
print(merged_df)

merged_df.to_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/merged.csv')
