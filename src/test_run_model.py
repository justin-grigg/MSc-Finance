
def old_setlogger(name, level):
    import logging
    # clearlogger()
    # global_model_name = name
    log = logging.getLogger(name)
    fhandler = logging.FileHandler(filename=f'logs/{name}-{logging.getLevelName(level)}.log') #, mode='a')
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fhandler.setFormatter(formatter)
    log.setLevel(level)
    log.addHandler(fhandler)
    return log

def setlogging(name, level):
    import logging
    # clearlogger()
    # global_model_name = name
    logger = logging.getLogger(name)
    fhandler = logging.FileHandler(filename=f'./logs/{name}-{level}.log') #, mode='a')
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)
    logger.setLevel(level)
    return logger

def test_again():
    pass

def test_write_to_log():
    pass

    import logging
    # clearlogger()
    # global_model_name = name
    name = 'test_write_to_log_A'
    level = logging.INFO
    log = logging.getLogger(name)
    
    if (log.hasHandlers()):
        log.handlers.clear()
    
    fhandler = logging.FileHandler(filename=f'./logs/{name}-{logging.getLevelName(level)}.log') #, mode='a')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fhandler.setFormatter(formatter)
    log.addHandler(fhandler)
    log.setLevel(level)

    log.info('test')
    return log

    '''
    import logging
    logdebug = setlogging('test_write_to_log_3', logging.INFO)
    # loginfo = __setlogger('test_write_to_log_3', logging.INFO)
    # logging.getLogger('test_write_to_log_A').debug('debug test A')
    # logging.getLogger('test_write_to_log_B').info('info test B')
    
    logdebug('test_write_to_log_3').info('debug test 3')
    # loginfo('test_write_to_log_4').info('info test 4')
    '''

def test_get_model_results():

    from statsmodels.tsa.arima.model import ARIMA
    import nb_credit_spread as cslibrary
    
    cslib = cslibrary.creditspread()
    start_date = '2009-01-31' #'1990-01-31' # '2009-01-31'
    ytw_delta = cslib.get_ytw_from_date_delta(start=start_date, srcfile='src/YTW-All-Values.xlsx')
    endog_col = 'CS-Aaa-3MO-DCF'
    order = (1, 1, 0)
    endog, exog = ytw_delta[endog_col], None
    model = ARIMA(endog=endog, exog=exog, order=order, trend='ct')
    model_fit = model.fit()
    import logging
    # log = setlogging('test_get_model_results', logging.INFO)
    log = old_setlogger('test_get_model_results', logging.INFO)
    # logging.getLogger('test_get_model_results').info('test')

    log.info(model_fit.summary())
    
    if (log.hasHandlers()):
        log.handlers.clear()