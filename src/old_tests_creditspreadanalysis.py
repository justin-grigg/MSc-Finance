'''
unit tests for credit spread analysis
'''
def test_call_AR():
    ''' call AR analysis '''
    import creditspreadanalysis as cr
    ar = cr.ARModel()
    ar.summary()

def test_call_RunDF():
    ''' call dickey fuller '''
    import creditspreadanalysis as cr
    st = cr.Stationarity()
    st.dickeyFuller()

def test_call_RunCommonStats():
    ''' call common stats '''
    import creditspreadanalysis as cr
    c = cr.Source()
    c.CommonStats(1)

def test_call_RunCorrelationPlots():
    ''' call correlation plots '''
    import creditspreadanalysis as cr
    c = cr.Correlation()
    c.AcfPacfPlotAll()
