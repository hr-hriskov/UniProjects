import pandas as pd
import numpy as np

# From CSV file to list of measurements
def preprocess(csv_file, time_list, time_limit):
    path = r"CSV files/"

    # reads csv file
    raw_data = pd.read_csv(path+csv_file)
    
    # drops unnecessary columns
    data = raw_data.drop(columns=["Status", "Units", "Alert ID", "Priority"])
    
    # splits into Date and Time columns
    data[['Date','Time']] = data.Time.str.split(expand=True)
    
    # adds Hours, Minutes and Seconds columns
    data[['Hours','Minutes', 'Seconds']] = data.Time.str.split(":", expand=True)
    data["Hours"] = data["Hours"].astype(int)
    data["Minutes"] = data["Minutes"].astype(int)
    data["Seconds"] = data["Seconds"].astype(int)
    
    # adding Timeline column
    data['Timeline'] = data["Hours"]*3600 + data["Minutes"]*60 + data["Seconds"]
    data["Timeline"] = data["Timeline"].astype(int)
    
    # Spliting the data into two Gauges
    gauge1 = data[(data["Object Name"] == "TIC Gauge 1")]
    gauge2 = data[(data["Object Name"] == "TIC Gauge 2")]
    
    # Reindexing dataframes
    gauge1.index = np.arange(1, len(gauge1) + 1)
    gauge2.index = np.arange(1, len(gauge2) + 1)
    
    gauge1_list = []
    gauge2_list = []
    
    for row in time_list:
        # divides into measurements
        g11 = gauge1[(gauge1.Time > row)]
        g11 = g11.head(time_limit)
        g22 = gauge2[(gauge2.Time > row)]
        g22 = g22.head(time_limit)
        
        # checks for unequal number of rows
        [g11, g22] = to_evenrows(g11, g22)
        
        # adds to a list
        gauge1_list.append(g11)
        gauge2_list.append(g22)
    
    return gauge1_list, gauge2_list, gauge1, gauge2


def to_evenrows(h1, h2):
    
    if len(h1.index) > len(h2.index):
        h1 = h1.iloc[:-1 , :]
    if len(h1.index) < len(h2.index):
        h2 = h2.iloc[:-1 , :]
        
    return h1, h2


def to_evenrows_list(l1, l2):
    
    if len(l1) > len(l2):
        l1 = l1.iloc[:-1]
    if len(l1) < len(l2):
        l2 = l2.iloc[:-1]
        
    return l1, l2


# finding every gauge2 0-point value in dataframe
def find_np_g2(g2, np_list):
    
    #converting list in array
    n_array = np.array(np_list)
    
    #finding 0-points
    g2_np = g2[g2['Timeline'].isin(n_array)]
    
    #filtering out copies
    g2_np = g2_np[(g2_np.Timeline.diff(periods=1) != 0)]
    
    #removing Hours, Minutes and Seconds columns
    g2_np = g2_np.drop(columns=["Hours", "Minutes", "Seconds"])
    
    #reindexing
    g2_np.index = np.arange(0, len(g2_np))
    
    return g2_np


# finding the Druckdifferenz
def Gauge1Diff(g1, np_list, hp_list):
    
    #converting list in array
    n_array = np.array(np_list)
    h_array = np.array(hp_list)
    
    #finding 0-points
    g1_np = g1[g1['Timeline'].isin(n_array)]
    g1_hp = g1[g1['Timeline'].isin(h_array)]
    
    #filtering out copies
    g1_np = g1_np[(g1_np.Timeline.diff(periods=1) != 0)]
    g1_hp = g1_hp[(g1_hp.Timeline.diff(periods=1) != 0)]
    
    #removing Hours, Minutes and Seconds columns
    g1_np = g1_np.drop(columns=["Hours", "Minutes", "Seconds"])
    g1_hp = g1_hp.drop(columns=["Hours", "Minutes", "Seconds"])
    
    #reindexing
    g1_np.index = np.arange(0, len(g1_np))
    g1_hp.index = np.arange(0, len(g1_hp))
    
    #difference calculation
    g1_diff = (g1_hp.Value - g1_np.Value).astype(float)
    
    return g1_diff
#     return g1_hp.Value