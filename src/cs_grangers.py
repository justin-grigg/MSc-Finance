'''
'''
def grangers_causation(cs_data):
    '''
    '''
    import pandas as pd
    import numpy as np
    import cs_logger as cslog
    from statsmodels.tsa.stattools import grangercausalitytests

    maxlag=12
    test = 'ssr_chi2test'
    debug = True

    variables = cs_data.columns
    df = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    data = cs_data

    for c in df.columns:
        for r in df.index:
            test_result = grangercausalitytests(data[[r, c]], maxlag=maxlag, verbose=False)
            p_values = [round(test_result[i+1][0][test][1],4) for i in range(maxlag)]
            # if verbose: print(f'Y = {r}, X = {c}, P Values = {p_values}')
            if debug: cslog.info(f'Y = {r}, X = {c}, P Values = {p_values}')
            min_p_value = np.min(p_values)
            df.loc[r, c] = min_p_value
    
    df.columns = [var + '_x' for var in variables]
    df.index = [var + '_y' for var in variables]
    
    return df