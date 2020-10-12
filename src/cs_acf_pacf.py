'''
'''
def acf_plot(cs_data, header):
    '''
    '''
    import statsmodels.api as sm
    import matplotlib.pylab as plt
    import cs_logger as cslog
    import seaborn as sns
    sns.set()

    df = cs_data
    r = df[header]

    fig = plt.figure(figsize=(12,8))
    lags = 40
    
    plotAcf = fig.add_subplot(111)
    fig = sm.graphics.tsa.plot_acf(r, lags=lags, ax=plotAcf)
    title = "%s for %s lags %s" % ("Autocorrelation", header, lags)
    plotAcf.set_title(title)

    #plt.show()
    f = "%s-%s-lag-%s.png" % (header, "corr-plot", lags)
    f = f"plots/{header}-acf-corr-plot-lag-{lags}.png"
    # fig.savefig("%s/%s" % (self.output, f))
    fig.savefig(f"{f}")
    cslog.info('%s figure done' % (f))
    plt.close('all')

def pacf_plot(cs_data, header):
    '''
    '''
    import statsmodels.api as sm
    import matplotlib.pylab as plt
    import cs_logger as cslog
    import seaborn as sns
    sns.set()

    df = cs_data
    r = df[header]

    fig = plt.figure(figsize=(12,8))
    lags = 40

    plotPacf = fig.add_subplot(111)
    fig = sm.graphics.tsa.plot_pacf(r, lags=lags, ax=plotPacf)
    title = "%s for %s lags %s" % ("Partial Autocorrelation", header, lags)
    plotPacf.set_title(title)
    #plt.show()
    f = "%s-%s-lag-%s.png" % (header, "corr-plot", lags)
    f = f"plots/{header}-pacf-corr-plot-lag-{lags}.png"
    # fig.savefig("%s/%s" % (self.output, f))
    fig.savefig(f"{f}")
    cslog.info('%s figure done' % (f))
    plt.close('all')

def acf_pacf_plot(cs_data, header):
    '''
    '''
    import statsmodels.api as sm
    import matplotlib.pylab as plt
    import logging
    import cs_logger as cslog
    import seaborn as sns

    log = logging.getLogger(cslog.acf_pacf_plots_stats_log)
    
    sns.set()

    df = cs_data
    r = df[header]

    fig = plt.figure(figsize=(12,8))
    lags = 40

    plotAcf = fig.add_subplot(211)  # specfies row and column index of sub-plot
    fig = sm.graphics.tsa.plot_acf(r, lags=lags, ax=plotAcf)
    
    title = "%s for %s lags %s" % ("Autocorrelation", header, lags)
    plotAcf.set_title(title)

    plotPacf = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(r, lags=lags, ax=plotPacf)
    title = "%s for %s lags %s" % ("Partial Autocorrelation", header, lags)
    plotPacf.set_title(title)
    # plt.show()
    
    f = "%s-%s-lag-%s.png" % (header, "corr-plot", lags)
    f = f"plots/{header}-corr-plot-lag-{lags}.png"

    saveplot(fig, f)

    log.info(f"{f} saved")

def saveplot(fig, name):
    import statsmodels.api as sm
    import matplotlib.pylab as plt
    import seaborn as sns

    fig.savefig(f"{name}")
    plt.close('all')

