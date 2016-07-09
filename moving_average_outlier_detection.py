import pandas as pd
import numpy as np

def voter_func(my_series):
    if my_series[0] == 1 and sum(my_series)/float(len(my_series)) >= 0.5:
        return int(1)
    else:
        return my_series[-1]

def detect_episode(df, window_size=30, use_global_mean = False):
    # df contains date and bpm

    df.loc[:,'mm'] = pd.Series.rolling(df['bpm'], window=window_size).mean()
    df.loc[:,'ss'] = pd.Series.rolling(df['bpm'], window=window_size).std()
       
    means = list(df.mm)
    stds = list(df.ss)
    
    diagnosis = [0 for i in xrange(window_size)]
        
    if use_global_mean:
        global_mean = df['bpm'].mean()
        global_std = df['bpm'].std()
        
        for i in xrange(window_size, len(means)):
            if means[i] > global_mean + 3*global_std:
                diagnosis.append(1)
            else:
                diagnosis.append(0)
    else:
        df.loc[:,'cum_mean'] = pd.Series.expanding(df['bpm'], window_size).mean()
        df.loc[:,'cum_std'] = pd.Series.expanding(df['bpm'], window_size).std()
        
        cum_means = list(df.cum_mean)
        cum_stds = list(df.cum_std)
    
        for i in xrange(window_size, len(means)):
            if means[i] >= cum_means[i-1] + 3*cum_stds[i-1] :
                diagnosis.append(1)
                cum_stds[i] = cum_stds[i-1]            
            else:
                diagnosis.append(0)

    df.loc[:,'diagnosis'] = diagnosis
    df.loc[:,'diagnosis2'] = pd.Series.rolling(df['diagnosis'], 4).apply(voter_func)
    return df
