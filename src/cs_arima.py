'''
ARIMA model for AR analysis
'''
def arima_model(cs_data):
    '''
    run ARIMA for with AR(1) first difference
    returns: dataframe [cs, const coef, AR coef]
    '''
    
    import pandas as pd
    import cs_logger as cslog
    import logging

    from statsmodels.tsa.arima_model import ARIMA

    logging.getLogger(cslog.arima_model_log).info('#### start AR(1) ####')

    cs_df = cs_data
    
    ar_result_lst = []   # create list for results

    for cs_col in cs_df.columns:
        # if not cs_col.startswith('CS_'):
            ar_model = ARIMA(endog=cs_df[cs_col].values, order=(1,0,0)) # AR(1)
            ar_result = ar_model.fit(disp=False)
            # logging.getLogger(cslog.arima_model_log).info('column: %s %s' % (cs_col, ar_result.summary())) # return an ARIMA model result summary for each column
            # logging.getLogger(cslog.arima_model_log).info(f"{cs_col}: {ar_result.params}")   # params 2x1 result; const, AR coef.
            ar_result_lst.append([cs_col, ar_result.params[0], ar_result.params[1]])
    
    ar_result_df = pd.DataFrame(ar_result_lst, columns=['column', 'const.coef', 'ar(1).coef']) #, index=ar_result_lst[0])
    ar_result_df.set_index('column', inplace=True)
    
    logging.getLogger(cslog.arima_model_log).info('#### AR(1) complete ####')
    return ar_result_df
