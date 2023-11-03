import pandas as pd
import numpy as np

GB = pd.read_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/GB.csv')
SPF = pd.read_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/SPF.csv')
FRED = pd.read_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/FRED.csv')

#Remove the first two columns of GB and SPF that capture dates and indexing
GB = GB.iloc[:, 2:]
SPF = SPF.iloc[:, 2:]

#Remove first row of FRED
FRED = FRED.iloc[1:,:]

GB.reset_index(drop=True, inplace=True)
SPF.reset_index(drop=True, inplace=True)
FRED.reset_index(drop=True, inplace=True)

merged_df = pd.concat([FRED, GB, SPF], axis=1)
print(merged_df.shape)
print(merged_df)

merged_df.to_csv('/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/merged.csv')
