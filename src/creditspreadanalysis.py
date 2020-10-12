''' credit spread analysis '''
# http://www.blackarbs.com/blog/time-series-analysis-in-python-linear-models-to-garch/11/1/2016#AR

import cs_logger as log

class Source:
    output = 'output'

    def __init__(self):
        import pandas as pd
        r = pd.read_excel(r'../all-data-combined.xlsx', sheet_name='CreditSpread', header=0)
        self.df = pd.DataFrame(r)

    def data(self):
        return(self.df)
    
        # ouput common stats and 
    def CommonStats(self, previousPeriod):
        log.info('***** CommonStats started *****')
        
        p = previousPeriod
        d = self.data()
        
        f = 'common-stats.csv'
        d.describe(include='all').transpose().to_csv('%s/%s' %(self.output, f))
        log.info('%s created' % (f))

        f = 'common-stats-delta-period-minus-%s.csv' % (p)
        d.diff(periods=p).describe(include='all').transpose().to_csv("%s/%s" % (self.output, f))
        log.info('%s created' % (f))

        f = 'data-period-minus-%s.csv' % (p)
        d.diff(periods=p).to_csv("%s/%s" % (self.output, f))
        log.info('%s created' % (f))
        
        log.info('***** CommonStats done *****')

class ARModel(Source):

    def summary(self):
        from statsmodels.tsa.arima_model import ARIMA

        df = self.df
        df = df.drop(df.columns[0],axis=1)  # drop datetime column
        for c in df.columns:
            model = ARIMA(df[c].values, order=(1,0,0)) # AR(1)
            m = model.fit(disp=0)
            log.info('column: %s %s' % (c, m.summary())) # return an ARIMA model result summary for each column
            log.info('%s: %s' % (c, m.params))

class Correlation(Source):
    
    output = 'output'
    # iterate all columns and output ACF and PACF to file
    def AcfPacfPlotAll(self):
        log.info('***** AcfPacfPlot started *****')
        
        for col in self.data().columns:
            if col != 'Date':
                self.AcfPacfPlot(col)
        
        log.info('***** AcfPacfPlot done *****')

    def AcfPacfPlot(self, header):
        import statsmodels.api as sm
        import matplotlib.pylab as plt
        df = self.data()
        r = df[header]

        fig = plt.figure(figsize=(12,8))
        lags = 40
        
        plotAcf = fig.add_subplot(211)
        fig = sm.graphics.tsa.plot_acf(r, lags=lags, ax=plotAcf)
        title = "%s for %s lags %s" % ("Autocorrelation", header, lags)
        plotAcf.set_title(title)

        plotPacf = fig.add_subplot(212)
        fig = sm.graphics.tsa.plot_pacf(r, lags=lags, ax=plotPacf)
        title = "%s for %s lags %s" % ("Partial Autocorrelation", header, lags)
        plotPacf.set_title(title)
        #plt.show()
        f = "%s-%s-lag-%s.png" % (header, "corr-plot", lags)
        fig.savefig("%s/%s" % (self.output, f))
        log.info('%s figure done' % (f))
        plt.close('all')

class Stationarity(Source):
    def dickeyFuller(self):
        ''' moved to cs_data_analysis.py '''
        pass
    
        import pandas as pd
        from statsmodels.tsa.stattools import adfuller
        df = self.df
        df = df.drop(df.columns[0],axis=1)  # drop datetime column
        
        for c in df.columns:
            dftest = adfuller(df[c].values) #, autolag='AIC')
        
            dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
            for key,value in dftest[4].items():
                dfoutput['Critical Value (%s)'%key] = value
            log.info('%s: ' % (c))
            log.info(dfoutput)

def RunAR():
    ar = ARModel()
    ar.summary()

def RunDF():
    st = Stationarity()
    st.dickeyFuller()

def RunCommonStats():
    c = Source()
    c.CommonStats(1)

def RunCorrelationPlots():
    c = Correlation()
    c.AcfPacfPlotAll()

if __name__ == "__main__":
    #RunAR()
    RunDF()
#    RunCommonStats()
#    RunCorrelationPlots()
    


    