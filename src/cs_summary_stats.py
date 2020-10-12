'''
cover summary statistics
'''

def summary_stats(cs_data):
    '''
    return summary stats (mean min, max, stddev) as dataframe
    '''
    import numpy as np
    import pandas as pd

    cs_df = cs_data
    cs_mean = cs_df.mean(axis=0)
    cs_stddev = np.std(cs_df, axis=0)
    cs_min = cs_df.min(axis=0)
    cs_max = cs_df.max(axis=0)
    cs_stat_df = pd.concat([cs_mean, cs_stddev, cs_min, cs_max], axis=1)
    cs_stat_df.columns = ['mean', 'stddev', 'min', 'max']
    
    return cs_stat_df

def summary_stats_full(cs_data):
    '''
    '''
    cs = cs_data
    cs_p0 = cs.describe(include='all').T
    # cs_p0.set_index(cs_p0.columns[0], inplace=True)  # set first column as index

    cs_diff = cs.diff(periods=1)
    cs_p1 = cs_diff.describe(include='all').T
    # cs_p1.set_index(cs_p1.columns[0], inplace=True)  # set first column as index

    return cs_p0, cs_p1