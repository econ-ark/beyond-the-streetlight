import pandas as pd
import numpy as np

merged = pd.read_csv("/Users/dc/Library/CloudStorage/OneDrive-JohnsHopkins/research/GitHub/dedwar65/RS100_Discussion/data/output/merged.csv")

merged = merged.iloc[:, 1:] # throw away first column with indexing

print(merged)