# src/growclonego/core.py
import pandas as pd
import numpy as np

def load_data(file_path: str):
    """
    Loads raw data from the given file path.

    Data must be formatted in either:
    - Wide format such that the first column is called 'barcode' and contains unique entries
    and the other column names indicate the time point (in days) and the numerical entries represent the 
    percent (0-100%) of each barcode at each timepoint.

    - Long format such that columns represent 'barcode', 'time' in days, and 'percent' (0-100%) abundance.
    
    Args:
        file_path (str): Path to the csv to load.
    
    Returns:
        pd.DataFrame: Loaded data as a Pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise ValueError(f"Error loading data from {file_path}: {e}")
   

def make_long(df):
    # Check if 'percent' is one of the column names
    if 'percent' in df.columns:
        # keep long formatted data
        df_long = df 
    if 'percent' not in df.columns:
        # convert wide data to long format
        df_long = df.melt(id_vars=df.columns[0], var_name='time', value_name='percent')
    return df_long


def est_growth(df_long, pop0=1e3, popf=30e3, mean_pop_rate=0.02):
    """
    this is documentation
    
    Args:
        asdf
    
    Returns:
        asdf
    """
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

    
    ##########
    # cannot estimate growth using on final timepoint as N0, remove these rows
    #df_long = df_long[df_long['time'] != df.columns[-1]]

    # ensure time is numeric
    df_long['timef'] = pd.to_numeric(df_long['timef'], errors='coerce')
    df_long['time'] = pd.to_numeric(df_long['time'], errors='coerce')
    
    # cannot estimate growth using on final timepoint as N0, remove these rows
    #df_long = df_long[df_long['time']] != pd.to_numeric(df_long['time']).max()
    df_long = df_long[df_long['time'] != pd.to_numeric(df_long['time']).max()]

    # create a new column with duration between time points conerted to hours
    df_long['interval_duration'] = 24*(df_long['timef']-df_long['time'])

    ####################################
    ######### ESTIMATE CELL COUNTS AND GROWTH RATE

    # # estimate initial cell count
    # df_long['est_N'] = df_long['prop']*pop0

    # # estimate final cell count
    # df_long['est_Nf'] = df_long['propf']*popf

    # # convert 0 counts to 1 cell to avoid NaN growth estimates
    # df_long.loc[df_long['est_N'] == 0, 'est_N'] = 1
    # df_long.loc[df_long['est_Nf'] == 0, 'est_Nf'] = 1

    # estimate exponential growth rate
    # undetected cells will produce NaNs
    with np.errstate(divide='ignore', invalid='ignore'):
        #df_long['est_r'] = (1 / df_long['interval_duration']) * np.log(df_long['est_Nf'] / df_long['est_N'])
        df_long['est_r'] = (1 / df_long['interval_duration']) * np.log(df_long['propf'] / df_long['prop'])
    

    # df_long['diff'] = df_long['est_r'] - df_long['est_r_prop']
    df_long['est_r_scaled'] = mean_pop_rate + df_long['est_r']

    # print(df_long['est_r_scaled'])

    return df_long
    


def summarize_growths(df_long):
    """
    Summarizes growth rates by barcode.

    Args:
        df_long (pd.DataFrame): Long formatted data with estimated growth rates.
    
    Returns:
        pd.DataFrame: Summary of growth rates by barcode.
    """
    # Group by barcode and calculate median growth rate from timepoints with informative (i.e. non-zero) data
   # summary = df_long[(df_long['prop'] != 0) & (df_long['propf'] != 0)].groupby('barcode')['est_r'].agg(med_r=('est_r', 'median'), n_timepoints=('est_r', 'size')).reset_index()
    summary = (
    df_long[(df_long['prop'] != 0) & (df_long['propf'] != 0)]
    .groupby('barcode')
    .agg(med_r=('est_r', 'median'), n_timepoints=('est_r', 'size'))
    .reset_index()
)
    return summary