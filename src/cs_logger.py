
adf_log = 'adf.stat.pvalue'
adf_fd_log = 'adf.stat.pvalue.firstdiff'
arima_model_log = 'arima.model'
summary_stats_log = 'summary.stats'
summary_stats_full_log = 'summary.stats.full'
acf_pacf_plots_stats_log = 'acf.pacf.plots.stats'
causation_log = 'grangers_causation.output'
cointegration_log = 'conintegration.stats'
lag_selection_log = 'lag.selection'

def getlogger(name):
    import logging
    return logging.getLogger(name)

def info(message):
    import logging
    # print(message)
    logging.info(message)

def debug(message):
    import logging
    # logging.debug(message)
    pass # print(message)
