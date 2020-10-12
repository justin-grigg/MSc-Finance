'''
credit spread analysis functions
'''

def get_credit_spread():
    '''
    load data from source file into dataframe. returns dataframe with date column index
    '''
    import pandas as pd
    import cs_logger as cslog

    source_file = r'src/YTW-All-Values.xlsx'
    # src_file = pd.read_excel(r'/Users/Justin/Desktop/git-hub-justin-grigg/testPythonDissAnalysis/src/all-data-combined.xlsx', sheet_name='CreditSpread', header=0)
    # src_file = pd.read_excel(r'all-data-combined.xlsx', sheet_name='CreditSpread', header=0)
    src_file = pd.read_excel(source_file, sheet_name='CreditSpread', header=0)
    cs_df = pd.DataFrame(src_file)
    cs_df = cs_df.set_index(pd.DatetimeIndex(cs_df['Date']))
    cs_df = cs_df.drop(cs_df.columns[0], axis=1)  # dataframe index set to date so column can be dropped 
    cslog.debug(f"df: {cs_df.head()}")
    
    return cs_df

def get_ytw_from_date(fromdate, srcfile=r'src/YTW-All-Values.xlsx'):
    '''
    load data from source file into dataframe
    columns:
        Corp - corporate bond rate
        TB - treasury bond rate
        CS - credit spread
        Econ - economic data
    '''

    import nb_credit_spread as cslibrary
    cslib = cslibrary.creditspread()
    return cslib.get_ytw_from_date_delta(srcfile=srcfile)

    import pandas as pd
    import cs_logger as cslog

    source_file = srcfile
    src_file = pd.read_excel(source_file, sheet_name='data', header=0, index_col='Date')
    ytw_df = pd.DataFrame(src_file)
    ytw_df = ytw_df.asfreq(pd.infer_freq(ytw_df.index)) # infer data frequency; monthly
    
    start_date = pd.to_datetime(fromdate)
    ytw_df = ytw_df[start_date:]    # filter records by date

    cslog.debug(f"df: {ytw_df.head()}")
    return ytw_df

def get_ytw():
    '''
    '''
    import pandas as pd
    ytw_df = get_ytw_from_date('1990-01-31')
    # start_date = pd.to_datetime('1990-01-31')
    # ytw_df = ytw_df[start_date:]    # filter records by date
    return ytw_df

def adf_stat_p_value(cs_df):
    from cs_unit_root import adf_stat_p_value

    ct = ['nc', 'c', 'ct', 'ctt']
    signif = [0.05, 0.01]
    autolog = 'BIC'

    for i in ct:
        for j in signif:
            # cover CS, CS-DCF and first diff
            adf_stat_p_value(cs_data=cs_df, column_prefix='CS-', auto_lag=autolog, signif=j, regress=i)
            # adf_stat_p_value(cs_data=i, column_prefix='Corp-', auto_lag=autolog, signif=j, regress=i)
            # cover TB and TB first diff
            adf_stat_p_value(cs_data=cs_df, column_prefix='TB-', auto_lag=autolog, signif=j, regress=i)

def arima_model(cs_df):
    '''
    run ARIMA for with AR(1) first difference
    returns: dataframe [cs, const coef, AR coef]
    '''
    from cs_arima import arima_model
    # cs_df = get_credit_spread()
    # cs_df = get_ytw()
    return arima_model(cs_df)

def summary_stats(df):
    '''
    return summary stats (mean min, max, stddev) as dataframe
    '''
    import cs_summary_stats as stats
    return stats.summary_stats(df)

def summary_stats_full(df):
    import cs_summary_stats as stats
    return stats.summary_stats_full(df)

def correlation_acf(df, column_prefix='CS-'):
    '''
    generate autocorrelation plots
    '''
    import cs_acf_pacf as acf
    import cs_logger as cslog
    import logging as logging

    log = logging.getLogger(cslog.acf_pacf_plots_stats_log)
    log.info('***** AcfPlot started *****')
    
    cs_df = df
    prefix = column_prefix

    for cs_column in cs_df.columns:
        if cs_column.startswith(prefix):
            acf.acf_plot(cs_df, cs_column)
    
    cslog.info('***** AcfPlot done *****')

def correlation_pacf(df, column_prefix='CS-'):
    '''
    generate partial autocorrelation plots
    '''
    import cs_acf_pacf as pacf
    import cs_logger as cslog
    import logging

    log = logging.getLogger(cslog.acf_pacf_plots_stats_log)
    log.info('***** PacfPlot started *****')
    
    cs_df = df
    prefix = column_prefix

    for cs_column in cs_df.columns:
        if cs_column.startswith(prefix):
            pacf.pacf_plot(cs_df, cs_column)
    
    log.info('***** PacfPlot done *****')

def correlation_acf_pacf(df, column_prefix='CS-'):
    '''
    generate partial autocorrelation plots
    '''
    import cs_acf_pacf as pacf
    import cs_logger as cslog
    import logging

    log = logging.getLogger(cslog.acf_pacf_plots_stats_log)
    log.info('***** Acf and Pacf Plot started *****')
    
    cs_df = df
    prefix = column_prefix

    for cs_column in cs_df.columns:
        if cs_column.startswith(prefix):
            pacf.acf_pacf_plot(cs_df, cs_column)
    
    log.info('***** Acf and Pacf done *****')

def print_full(df, logger):
    '''
    write contents of dataframe to logger
    '''
    import pandas as pd
    import logging

    pd.set_option('display.max_rows', len(df))
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.6f}'.format)
    pd.set_option('display.max_colwidth', None)
    logger.info(df)

def causation(df):
    '''
    '''
    from cs_causation import grangers_causation
    return grangers_causation(df)

def conintegration(ytw):
    '''
    '''
    from cs_conintegration import johanson_cointegration_test

    '''
    df_corp = cs_df[['Corp-Aaa_Corp', 'Corp-Aa_Corp', 'Corp-A_Corp', 'Corp-Baa_Corp']]
    df_corp = cs_df[['Econ-UNRATE', 'Econ-DSPIC96', 'Econ-CPIAUCSL', 'Econ-CPILFESL', 'Econ-INDPRO', 'Econ-PCE']]
    df_corp = cs_df[['Market-SP500', 'Market-SP500-change', 'Market-RMRF']]
    '''
    # df_cs = cs_df[['CS-Aaa-3MO', 'CS-Aa-3MO', 'CS-A-3MO', 'CS-Baa-3MO', 'CS-Aaa-1YR', 'CS-Aa-1YR', 'CS-A-1YR', 'CS-Baa-1YR', 'CS-Aaa-5YR', 'CS-Aa-5YR', 'CS-A-5YR', 'CS-Baa-5YR']]
    # johanson_cointegration_test(df_cs)
    # df_tb = cs_df[['TB-3MO-TY', 'TB-1YR-TY', 'TB-5YR-TY']]
    # johanson_cointegration_test(df_tb)

    johanson_cointegration_test(ytw[ ['CS-Aa-3MO', 'TB-3MO-TY'] ])

def main():
    '''
    main module method
    '''
    import logging, sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    
    import cs_logger as log
    
    log.info('calling...')
    adf_stat_p_value()
    # arima_model()
    # print_full(summary_stats())
    # arima_model()
    # print_full(arima_model())
    log.info('done')

if __name__ == "__main__":
    main()
