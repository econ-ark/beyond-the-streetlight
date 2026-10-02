# Produce data/output/FRED.csv, the realized values of the forecasted variables.
#
# By default this copies data/raw/FRED_snapshot.csv: the FRED vintage retrieved on
# 2023-11-03 (commit 47eb307) that the published results use. That keeps the
# pipeline offline and key-free. Pass --refresh, with FRED_API_KEY set, to download
# current data instead; FRED revises these series, so refreshed results will
# differ somewhat from the committed ones.
import os
import shutil
import sys

import pandas as pd

snapshot = 'data/raw/FRED_snapshot.csv'
output = 'data/output/FRED.csv'

if '--refresh' not in sys.argv[1:]:
    shutil.copyfile(snapshot, output)
    print(f"Using FRED snapshot {snapshot} (pass --refresh to download current data)")
    sys.exit(0)

api_key = os.environ.get('FRED_API_KEY')
if not api_key:
    sys.exit("FRED_API_KEY is not set. Get a free key at "
             "https://fred.stlouisfed.org/docs/api/api_key.html")

import fredpy as fp

fp.api_key = api_key
win =['01-01-1982','12-01-2017']
win2 = ['10-01-1981','12-01-2018']
unemp = fp.series("UNRATE").window(win2).as_frequency(freq='Q')

#pce_Q = fp.series("PCEPI").window(win2).apc().as_frequency(freq='Q')
#pce_core_Q = fp.series("PCEPILFE").window(win2).apc().as_frequency(freq='Q')

#grPCE_Q = fp.series("PCEC96").window(win).as_frequency(freq='Q').pc(annualized=True)
#grPCE_Q = fp.series("DPCERA3M086SBEA").window(win2).as_frequency(freq='Q').pc(annualized=True)
grPCE_Q = fp.series("DPCERA3Q086SBEA").window(win2).as_frequency(freq='Q').pc(annualized=True)

obs_df = pd.DataFrame({"Unemployment": unemp.data,
                   #"Inflation": pce_Q.data,
                   #"Core Inflation": pce_core_Q.data,        
                   "real Consumption Growth": grPCE_Q.data
})

print(obs_df.head)

decimal = False  # Set to the desired number of decimal places or False to disable formatting

if decimal is not False:
    for column in obs_df.columns[1:]:
        obs_df[column] = obs_df[column].apply(lambda x: f"{x:.{decimal}f}")

obs_df.to_csv(output)

# obs_df.to_excel('data/output/FRED_scraped.xlsx', index=False)