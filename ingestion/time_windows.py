import pandas as pd
import time
import os
import numpy as np
import statistics as stat
from math import pi
import random

# gets symbol name from csv file
def get_symbol(f_path):
    filename = os.path.basename(f_path)
    symbol_name = filename.split(".")[0]
    print("Loading:", symbol_name)
    return symbol_name

# returns a (symbol_name,dataframe) tuple
def load_csv(f_path,suppress=True):
    '''suppress : suppress output of the exchange and symbol name'''
    
    df = pd.read_csv(f_path,index_col=0,parse_dates=["Timestamp"])
    filename = os.path.basename(f_path)
    symbol_name = get_symbol(f_path)
    
    if not suppress:
        print("Symbol:",symbol_name)
    
    return (symbol_name,df)

def get_num_rows(df):
    return df.shape[0]

def rm_same_day_pumps(df):
    # Removes spikes that occur on the same day
    df = df.copy()
    df['Timestamp_DAYS'] = df['Timestamp'].apply(lambda x: x.replace(hour=0, minute=0, second=0))
    df = df.drop_duplicates(subset='Timestamp_DAYS', keep='last')
    return df

# adds a rolling average column with specified window size to a given df and col
def add_RA(df,win_size,col,name):
    df[name] = pd.Series.rolling(df[col],window=win_size,center=False).mean()

# finds volume spikes in a given df, with a certain threshold and window size
# returns a (boolean_mask,dataframe) tuple
def find_vol_spikes(df,v_thresh,win_size):
    # -- add rolling average column to df --
    vRA = str(win_size)+'h Volume RA'
    add_RA(df,win_size,'Volume',vRA)
    
    # -- find spikes -- 
    vol_threshold = v_thresh*df[vRA] # v_thresh increase in volume
    vol_spike_mask = df["Volume"] > vol_threshold # where the volume is at least v_thresh greater than the x-hr RA
    df_vol_spike = df[vol_spike_mask]
    
    return (vol_spike_mask,df_vol_spike)

# finds price spikes in a given df, with a certain threshold and window size
# returns a (boolean_mask,dataframe) tuple
def find_price_spikes(df,p_thresh,win_size):
    # -- add rolling average column to df --
    pRA = str(win_size)+'h Close Price RA'
    add_RA(df,win_size,'Close',pRA)
    
    # -- find spikes -- 
    p_threshold = p_thresh*df[pRA] # p_thresh increase in price
    p_spike_mask = df["High"] > p_threshold # where the high is at least p_thresh greater than the x-hr RA
    df_price_spike = df[p_spike_mask]
    return (p_spike_mask,df_price_spike)

# finds price dumps in a given df, with a certain threshold and window size
# requires a price rolling average column of the proper window size and naming convention
# returns a (boolean_mask,dataframe) tuple
def find_price_dumps(df,win_size):
    pRA = str(win_size)+"h Close Price RA"
    pRA_plus = pRA + "+" + str(win_size)
    
    df[pRA_plus] = df[pRA].shift(-win_size)
    price_dump_mask = df[pRA_plus] <= (df[pRA] + df[pRA].std())
    # if the xhour RA from after the pump was detected is <= the xhour RA (+std dev) from before the pump was detected
    # if the price goes from the high to within a range of what it was before
    
    df_p_dumps = df[price_dump_mask]
    return (price_dump_mask,df_p_dumps)

def find_volume_dumps(df,win_size):
    vRA = str(win_size)+"h Volume RA"
    vRA_plus = vRA + "+" + str(win_size)
    
    df[vRA_plus] = df[vRA].shift(-win_size)
    price_dump_mask = df[vRA_plus] <= (df[vRA] + df[vRA].std())
    # if the xhour RA from after the pump was detected is <= the xhour RA (+std dev) from before the pump was detected
    # if the volume goes from the high to within a range of what it was before
    
    df_p_dumps = df[price_dump_mask]
    return (price_dump_mask,df_p_dumps)

# returns final dataframe
def analyze_symbol(f_path, v_thresh, p_thresh, win_size=24, c_size='1h', plot=False):
    '''
    USAGE:
    f_path : path to OHLCV csv e.g.'data/binance/STORJ-BTC.csv'
    v_thresh : volume threshold e.g. 5 (500%)
    p_thresh : price threshold e.g. 1.05 (5%)
    c_size : candle size
    win_size : size of the window for the rolling average, in hours
    '''
    # load the data
    symbol_name,df = load_csv(f_path)

    # find spikes
    vmask,vdf = find_vol_spikes(df, v_thresh, win_size)
    num_v_spikes = get_num_rows(vdf) # num of volume spikes found for this symbol pair

    pmask,pdf = find_price_spikes(df, p_thresh, win_size)
    num_p_spikes = get_num_rows(pdf) # num of price spikes

    pdmask,pddf = find_price_dumps(df, win_size)
    vdmask,vddf = find_volume_dumps(df, win_size)

    # find coinciding price and volume spikes
    vp_combined_mask = (vmask) & (pmask)
    vp_combined_df = df[vp_combined_mask]
    num_vp_combined_rows = get_num_rows(vp_combined_df)

    # coinciding price and volume spikes for alleged P&D (more than 1x per given time removed)
    vp_combined_rm = rm_same_day_pumps(vp_combined_df)
    num_alleged = get_num_rows(vp_combined_rm)

    # find coinciding price and volume spikes with dumps afterwards
    final_combined_mask = (vmask) & (pmask) & (pdmask)
    final_combined = df[final_combined_mask]
    final_combined_rm = rm_same_day_pumps(final_combined)

    print("Detected P&Ds:\n" + final_combined_rm)
    num_final_combined = get_num_rows(final_combined_rm)

    row_entry = {
                'Symbol':symbol_name,
                'Price Spikes':num_p_spikes,
                'Volume Spikes':num_v_spikes,
                'Alleged Pump and Dumps':num_alleged,
                'Pump and Dumps':num_final_combined}

    return row_entry




print(analyze_symbol('data/binance/HARD-BTC.csv', 4, 1.05, win_size=12, c_size='1h', plot=False))
#print(analyze_symbol('../Research/Source1/data/binance/CDT-BTC.csv', 3, 1.05, win_size=12, c_size='1h', plot=False))



