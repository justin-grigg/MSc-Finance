'''
unit tests for credit spread analysis
'''
import logging
loggers = {}

def setup():
    '''
    test fixture setup
    '''
    # __removeloggers()

def setLogger(name, level):
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

def setlogfile(logger, level=logging.INFO):
    '''
    a logger is created based on logger parameter passed as an argument by the caller
    returns reference to logger
    '''
    return setLogger(logger, level)

def test_adf_stat_p_value():
    '''
    unit test for adf
    '''
    import cs_logger as cslog
    __run_adf_stat_p_value(cslog.adf_log)

def __run_adf_stat_p_value(logDest):

    import datetime
    import cs_data_analysis as cs
    import cs_logger as cslog
    log = setlogfile(logDest)

    try:
        now = datetime.datetime.now()
        log.info(f"{'-'*10} start {now:%Y-%m-%d %H:%M} {'-'*10}")

        import nb_credit_spread as cslibrary
        cslib = cslibrary.creditspread()

        srcfile = r'src/YTW-All-Values.xlsx'
        df = cslib.get_ytw_from_date_delta(srcfile=srcfile, start='2009-01-31')
        cs.adf_stat_p_value(df)
        
        log.info(f"{'-'*10} done {'-'*10}")
        assert True
    except:
        import sys
        message = f"Unexpected error: {sys.exc_info()[0]} {sys.exc_info()[1]}"
        log_error = setlogfile(logDest, logging.ERROR)
        log_error.error(message)
        raise

def test_arima_model():
    '''
    unit test for arima
    '''
    import cs_data_analysis as cs
    import cs_logger as cslog
    import logging

    log = setlogfile(cslog.arima_model_log)

    try:
        import nb_credit_spread as cslibrary
        cslib = cslibrary.creditspread()
        srcfile = r'src/YTW-All-Values.xlsx'
        df = cslib.get_ytw_from_date_delta(srcfile=srcfile, start='2009-01-31')

        return

        log.info('**** AR(1) ****')
        cs.print_full(cs.arima_model(df), log)

        log.info('**** AR(1) diff period 1 ****')
        cs_df = cs.get_ytw_from_date('1989-12-31')  # fetch month before 31 Jan 1990
        cs_df = cs_df.diff(periods=1)   # diff with previous period
        cs_df = cs_df['1990-01-31':]    # get only records from 31 Jan 1990; this avoids NaN in first row
        cs.print_full(cs.arima_model(cs_df), log)    # get AR(1) coefficients
        assert True

    except:
        import sys
        message = f"Unexpected error: {sys.exc_info()[0]} {sys.exc_info()[1]}"
        log.error(message)
        raise

def test_summary_stats():
    '''
    unit test for summary stats
    '''
    import cs_data_analysis as cs
    import cs_logger as cslog
    import logging 
    import nb_credit_spread as cslibrary
    
    cslib = cslibrary.creditspread()
    srcfile = r'src/YTW-All-Values.xlsx'
    ytw_df = cslib.get_ytw_from_date_delta(srcfile=srcfile, start='2014-01-31')
    cs.print_full(cs.summary_stats(ytw_df), setlogfile(cslog.summary_stats_log))
    
    assert True

def test_summary_stats_full():
    '''
    unit test for summary stats
    '''
    import cs_data_analysis as cs
    import cs_logger as cslog
    import logging 

    log = setlogfile(cslog.summary_stats_full_log)

    try:
        import nb_credit_spread as cslibrary
    
        cslib = cslibrary.creditspread()
        srcfile = r'src/YTW-All-Values.xlsx'
        ytw_df = cslib.get_ytw_from_date_delta(srcfile=srcfile, start='2014-01-31')

        cs_stats, cs_stats_p1 = cs.summary_stats_full(ytw_df)
        
        log.info('**** cs stats ****')
        cs.print_full(cs_stats, log)

        log.info('**** cs stats p1 diff ****')
        cs.print_full(cs_stats_p1, log)

        assert True
    except:
        import sys
        log.error(f"Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
        raise

def test_correlation_acf():
    '''
    '''
    import cs_data_analysis as cs
    import cs_logger as cslog
    
    log = setlogfile(cslog.acf_pacf_plots_stats_log)

    try:
        import nb_credit_spread as cslibrary

        cslib = cslibrary.creditspread()
        srcfile = r'src/YTW-All-Values.xlsx'
        ytw_df = cslib.get_ytw_from_date_delta(srcfile=srcfile, start='2009-01-31')

        cs.correlation_acf(ytw_df, 'CS-')
        assert True
    except:
        import sys
        log.error(f"Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
    raise

def test_correlation_pacf():
    '''
    '''
    import cs_data_analysis as cs
    import cs_logger as cslog
    
    log = setlogfile(cslog.acf_pacf_plots_stats_log)

    try:
        import nb_credit_spread as cslibrary

        cslib = cslibrary.creditspread()
        srcfile = r'src/YTW-All-Values.xlsx'
        ytw_df = cslib.get_ytw_from_date_delta(srcfile=srcfile, start='2009-01-31')

        cs.correlation_pacf(ytw_df, 'CS-')
        assert True
    except:
        import sys
        log.error(f"Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
    raise

def test_correlation_acf_pacf():
    '''
    '''
    import cs_data_analysis as cs
    import cs_logger as cslog
    
    log = setlogfile(cslog.acf_pacf_plots_stats_log)

    try:
        import nb_credit_spread as cslibrary

        cslib = cslibrary.creditspread()
        srcfile = r'src/YTW-All-Values.xlsx'
        ytw_df = cslib.get_ytw_from_date_delta(srcfile=srcfile, start='2009-01-31')

        cs.correlation_acf_pacf(ytw_df, 'CS-')

        assert True
    except:
        import sys
        log.error(f"Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
        raise

def test_causation_cs_pce():
    import cs_data_analysis as cs
    import cs_logger as cslog
    
    log = setlogfile(cslog.causation_log)
    try:
        import nb_credit_spread as cslibrary

        cslib = cslibrary.creditspread()
        srcfile = r'src/YTW-All-Values.xlsx'
        ytw_df = cslib.get_ytw_from_date_delta(srcfile=srcfile, start='2009-01-31')

        df = ytw_df[ ['CS-Aaa-3MO', 'Econ-PCE'] ]
        from cs_causation import grangers_causation
        r = grangers_causation(df)
        # print(r)
        cs.print_full(r, log)
        
        assert True
    except:
        import sys
        log.error(f"Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
        raise

def test_causation():
    '''
    '''
    import cs_data_analysis as cs
    import cs_logger as cslog
    
    log = setlogfile(cslog.causation_log)
    try:
        import nb_credit_spread as cslibrary

        cslib = cslibrary.creditspread()
        srcfile = r'src/YTW-All-Values.xlsx'
        ytw_df = cslib.get_ytw_from_date_delta(srcfile=srcfile, start='2009-01-31')

        cs.print_full(cs.causation(ytw_df), log)
        assert True
    except:
        import sys
        log.error(f"Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
        raise

def test_cointegration():
    '''
    '''
    import cs_data_analysis as cs
    import cs_logger as cslog

    log = setlogfile(cslog.cointegration_log)
    
    try:
        import nb_credit_spread as cslibrary

        cslib = cslibrary.creditspread()
        srcfile = r'src/YTW-All-Values.xlsx'
        ytw_df = cslib.get_ytw_from_date_delta(srcfile=srcfile, start='2009-01-31')

        cs.conintegration(ytw_df)
        #cs.print_full(cs.conintegration(), log)
        assert True
    except:
        import sys
        log.error(f"Unexpected error: {sys.exc_info()[0]}\n{sys.exc_info()[1]}")
        raise

def test_lag_selection():
    import cs_logger as cslog
    log = setlogfile(cslog.lag_selection_log)

    try:
        import cs_data_analysis as cs
        import cs_lag_selection as lag
        
        import datetime
        now = datetime.datetime.now()
        log.info(f"{'-'*10} start lag selection {now:%Y-%m-%d %H:%M} {'-'*10}")
        
        import nb_credit_spread as cslibrary

        cslib = cslibrary.creditspread()
        srcfile = r'src/YTW-All-Values.xlsx'
        ytw = cslib.get_ytw_from_date_delta(srcfile=srcfile, start='2009-01-31')

        cs = ['CS-Aaa', 'CS-Aa', 'CS-A', 'CS-Baa', 'CS-DCF-Aaa', 'CS-DCF-Aa', 'CS-DCF-A', 'CS-DCF-Baa']
        tb = ['3MO', '1YR', '5YR']

        for i in cs:
            for j in tb:
                lag.call_lag_selection(ytw, f"{i}-{j}", f"TB-{j}-TY")
                lag.call_lag_selection(ytw, f"{i}-{j}-diff", f"TB-{j}-TY")
        return
    except:
        import sys
        log.error(f"Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
        raise

def get_ytw_test():
    import os
    print(os.getcwd())
    import nb_credit_spread as cslibrary
    import logging
    cslib = cslibrary.creditspread()
    srcfile = 'src/YTW-All-Values.xlsx'
    srcfile = 'YTW-All-Values.xlsx'
    srcfile = f"{os.getcwd()}/src/YTW-All-Values.xlsx"
    start_date = '2009-01-31'
    return  cslib.get_ytw_from_date_delta(srcfile=srcfile, start=start_date)

def test_load_source_values():

    df = get_ytw_test()
    log = setlogfile('test.load.source.values', logging.INFO)

    from statsmodels.tsa.stattools import adfuller
    # adf_tstat, pvalue, tstat, results = adfuller(df['CS-Aaa-3MO'].values) # , maxlag=40, regression='ct', autolag='BIC', regresults=True)
    # print(adf_tstat)
    #print(pvalue)
    #print(tstat)
    #print(results)
    
    adf = adfuller(df['CS-Aaa-3MO'].values) # , maxlag=40, regression='ct', autolag='BIC', regresults=True)
    print(adf)
    
    from arch.unitroot import ADF
    adf = ADF(y=df['CS-Aaa-3MO'].values) #, lags=40, trend='ct', method='BIC')
    print(adf.pvalue)


    import cs_data_analysis as cs
    cs.print_full(df, log)
    pass
    '''
    import cs_data_analysis as cs
    cs.get_ytw()
    '''
def test_ARIMA():

    from statsmodels.tsa.arima.model import ARIMA

    df = get_ytw_test()

    model_fit = ARIMA(endog=df['CS-Aaa-3MO'], exog=None, order=(1,1,0), trend=None).fit()
    print(model_fit.summary())