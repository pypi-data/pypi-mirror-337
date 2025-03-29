import pandas as pd
import numpy as np
# import plotnine

####################################
######### READ IN DATA
# ensure data is formatted such that the first column is called 'barcode' and contains unique entries
# and the other column names indicate the time point (in days)
# numerical entries represent the percent (0-100%) of each barcode at each timepoint
df = pd.read_csv('data/test_data.csv', index_col=False)

# alternatively, data can be directly read in as long format with columns representing
# 'barcode', 'time' in days, and 'percent' abundance


### function to convert wide data to long
# ensure data is formatted such that the first column is called 'barcode' and contains unique entries
# and the other column names indicate the time point (in days)
# numerical entries represent the percent (0-100%) of each barcode at each timepoint

def make_long(df):
    df_long = df.melt(id_vars=df.columns[0], var_name='time', value_name='percent')
    
    return df_long


### function to calculate growth rate from barcode abundance data
# ensure data is formatted such that the first column is called 'barcode'

def est_growth(df_long, pop0=100e3, popf=100e3):
    ####################################
    ######### FORMAT DATA FOR CALCULATIONS

    # convert percent to proportion
    df_long['prop'] = df_long['percent']/100

    # convert NaNs to 0 
    df_long = df_long.fillna(0)

    # create new column of final proportion by shifting prop column up by one for each barcode
    df_long['propf'] = df_long.groupby('barcode')['prop'].shift(-1)

    # create new column of final time by shifting time column up by one for each barcode
    df_long['timef'] = df_long.groupby('barcode')['time'].shift(-1)

    # create a new column mapping the time interval
    df_long['interval'] = df_long['time'].astype(str) + '_' + df_long['timef'].astype(str)

    # cannot estimate growth using on final timepoint as N0, remove these rows
    df_long = df_long[df_long['time'] != df.columns[-1]]

    # ensure time is numeric
    df_long['timef'] = pd.to_numeric(df_long['timef'], errors='coerce')
    df_long['time'] = pd.to_numeric(df_long['time'], errors='coerce')

    # create a new column with duration between time points
    df_long['interval_duration'] = df_long['timef']-df_long['time']

    ####################################
    ######### ESTIMATE CELL COUNTS AND GROWTH RATE

    # estimate initial cell count
    df_long['est_N'] = df_long['prop']*pop0

    # estimate final cell count
    df_long['est_Nf'] = df_long['propf']*popf

    # # convert 0 counts to 1 cell to avoid NaN growth estimates
    # df_long.loc[df_long['est_N'] == 0, 'est_N'] = 1
    # df_long.loc[df_long['est_Nf'] == 0, 'est_Nf'] = 1

    # estimate exponential growth rate
    # undetected cells will produce NaNs
    with np.errstate(divide='ignore', invalid='ignore'):
        df_long['est_r'] = (1 / df_long['interval_duration']) * np.log(df_long['est_Nf'] / df_long['est_N'])
    
    return df_long
    

df_long = make_long(df)

est_growth(df_long)