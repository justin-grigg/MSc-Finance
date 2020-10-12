'''
covers unit root analysis
'''

def adf_stat_p_value(cs_data, column_prefix, auto_lag='AIC', signif=0.05, regress='ct'):
    ''' 
    calls ADF (Augmented Dickey Fuller) to return ADF stat and p-value. call on each column.
    verify if p-value is greater than ADF test statistic. returns stationarity at lag
    '''

    import pandas as pd
    import logging as log
    import cs_logger as cslog
    from statsmodels.tsa.stattools import adfuller

    log = log.getLogger(cslog.adf_log)
    log.debug(cs_data.head)

    cs_df = cs_data

    for col_data in cs_df.columns:
        if col_data.startswith(column_prefix):
            log.info(f"{'-'*10} Augmented Dickey-Fuller Test on '{col_data}' regression {regress} auto_lag {auto_lag} {'-'*10}")
            r = adfuller(cs_df[col_data].values, regression=regress, autolag=auto_lag)
            
            output = {'test_statistic':round(r[0], 4), 'pvalue':round(r[1], 4), 'n_lags':round(r[2], 4), 'n_obs':r[3]}
            
            adf_series = pd.Series(r[0:4], index=['Test Statistic:','p-value:','#Lags Used:','Number of Observations Used:'])

            adf_series['column:'] = col_data

            for key, value in r[4].items():
                adf_series['Critical Value (%s):'%key] = value

            adf_series['signif:'] = signif
            adf_series['autolag:'] = auto_lag
            adf_series['c-t-t:'] = regress

            # log.info(f"column: {col_data}")

            pvalue = f"{output['pvalue']}"

            if output['pvalue'] <= signif:
                statement = f"Series is Stationary. Null Hypothesis Rejecting"
            else:
                statement = f"Series is Non-stationary. Null Hypothesis Weak evidence reject"

            adf_series['Stationarity p-value:'] = pvalue
            adf_series['Summary:'] = statement

            log.info(adf_series)
