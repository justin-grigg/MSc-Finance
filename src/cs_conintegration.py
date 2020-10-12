'''
'''

def to_positive_definitive(M):
    import numpy as np

    M = np.matrix(M)
    M = (M + M.T) * 0.5
    k = 1
    I = np.eye(M.shape[0])
    w, v = np.linalg.eig(M)
    min_eig = float(v.min()) # cast numpy.complex128 to float
    M += (-min_eig * k * k + np.spacing(min_eig)) * I
    return M

def validate_positive_definitive(M):
    import numpy as np

    try:
        np.linalg.cholesky(M)
    except np.linalg.LinAlgError:
        M = to_positive_definitive(M)
    # Print the eigenvalues of the Matrix
    # print(np.linalg.eigvalsh(p))
    return M


def johanson_cointegration_test(df, alpha=0.05):
    '''
    perform Johanson's Cointegration test and report summary
    '''
    from statsmodels.tsa.vector_ar.vecm import coint_johansen

    import cs_logger as cslog

    log = cslog.getlogger(cslog.cointegration_log)
    # log.info('Name   ::  Test Stat > C(95%)    =>   Signif  \n', '--'*20)
    log.info('Name   ::  Test Stat > C(95%)    =>   Signif.')
    log.info('--'*20)

    # i = validate_positive_definitive(df.values[:])

    for c in df.columns:
        log.info(f"column {c}")
        c_valid = validate_positive_definitive(df[c].values[:])  # pass dataframe as matrix
        
        import pandas as pd
        df_c = pd.DataFrame(data=c_valid)
        print_df(df_c)

        # data = c_valid
        data = df_c
        out = coint_johansen(endog=data, det_order=-1, k_ar_diff=5) # n.b. Critical values are only available for time series with 12 variables at most
        d = {'0.90':0, '0.95':1, '0.99':2}
        traces = out.lr1 # trace statistic
        cvts = out.cvt[:, d[str(1-alpha)]]  # critical values

        def adjust(val, length= 10): return str(val).ljust(length)

        for col, trace, cvt in zip(c, traces, cvts):
            # log.info(adjust(col))
            summary = f"{adjust(col)}::{adjust(round(trace,2), 9)} > {adjust(cvt, 8)} => {trace > cvt}"
            log.info(summary)

    # Summary
    # print('Name   ::  Test Stat > C(95%)    =>   Signif  \n', '--'*20)
    # for col, trace, cvt in zip(df.columns, traces, cvts):
    #    print(adjust(col), ':: ', adjust(round(trace,2), 9), ">", adjust(cvt, 8), ' =>  ' , trace > cvt)

def print_df(df):
    import pandas as pd

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    print(df)