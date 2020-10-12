
def call_lag_selection(cs, corp, mat):
    import logging as logging
    import cs_logger as cslog
    
    aic, bic = lag_selection(cs, corp, mat)
    log = logging.getLogger(cslog.lag_selection_log)
    log.info(f'{corp}-{mat} aic: {aic} bic: {bic}')

def info(message):
    import logging as log
    import cs_logger as cslog
    logger = log.getLogger(cslog.lag_selection_log)
    logger.info(message)

def debug(message):
    return

def lag_selection(ytw, corp, tb):
    import cs_data_analysis as da
    from statsmodels.tsa.api import VAR
    import numpy as np
    '''
    CS-Aaa-3MO	 CS-Aa-3MO	 CS-A-3MO	 CS-Baa-3MO	 CS-Aaa-1YR	 CS-Aa-1YR	 CS-A-1YR	 CS-Baa-1YR	 CS-Aaa-5YR	 CS-Aa-5YR	 CS-A-5YR	 CS-Baa-5YR		 
    TB-3MO-TY	 TB-1YR-TY	 TB-5YR-TY
    '''
    debug(ytw.shape)
    endog = ytw[[corp, tb]]
    
    lag_count = 10
    ic_aic = np.zeros((lag_count, 1))  # AIC, BIC, HQIC
    ic_bic = np.zeros((lag_count, 1))

    for i in range(lag_count):
        debug(f"{'-'*4} period: {lag_count} {'-'*4}")
        # https://www.statsmodels.org/stable/generated/statsmodels.tsa.vector_ar.var_model.VAR.fit.html
        model = VAR(endog=endog)
        model_fit = model.fit(maxlags=i + 1, trend='ct', verbose=True)
        debug(f"aic: {model_fit.aic:.6f}")
        debug(f"bic: {model_fit.bic:.6f}")
        debug(f"hqic: {model_fit.hqic:.6f}")
        ic_aic[i] = model_fit.aic
        ic_bic[i] = model_fit.bic
        results = model_fit.summary()
        debug(results)

    ic_aic_min, aic_model_min = np.min(ic_aic), np.argmin(ic_aic)
    ic_bic_min, bic_model_min = np.min(ic_bic), np.argmin(ic_bic)

    debug('Relative Likelihoods')
    debug(np.exp((ic_aic_min - ic_aic) / 2))
    debug(f'number of parameters in minimum AIC model {(aic_model_min + 1)}')

    debug(np.exp((ic_bic_min - ic_bic) / 2))
    debug(f'number of parameters in minimum BIC model {(bic_model_min + 1)}')

    return aic_model_min + 1, bic_model_min + 1

