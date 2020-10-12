class creditspread:

    def load_source(self, srcfile=r'YTW-All-Values.xlsx'):
        import pandas as pd
        source_file = srcfile
        src_file = pd.read_excel(source_file, sheet_name='data', header=0, index_col='Date')
        ytw_df = pd.DataFrame(src_file)
        ytw_df = ytw_df.asfreq(pd.infer_freq(ytw_df.index)) # infer data frequency; monthly
        return ytw_df

    def get_ytw_from_date(self, start='1990-01-31', end='2019-07-31', srcfile=r'YTW-All-Values.xlsx'):
        '''
        load data from source file into dataframe
        columns:
            Corp - corporate bond rate
            TB - treasury bond rate
            CS - credit spread
            Econ - economic data
        '''
        import pandas as pd

        ytw_df = self.load_source()
        start_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end)
        ytw_df = ytw_df[start_date:end_date]    # filter records by date

        # cslog.debug(f"df: {ytw_df.head()}")
        return ytw_df

    def get_ytw_from_date_delta(self, start='1990-01-31', end='2019-07-31', srcfile=r'YTW-All-Values.xlsx'):
        
        import numpy as np
        import pandas as pd
        
        df = self.load_source(srcfile=srcfile)    # get entire source table

        # append CS diff, although these are not required
        df['CS-Aaa-3MO-diff'] = df['CS-Aa-3MO'].diff(periods=1)
        df['CS-Aa-3MO-diff'] = df['CS-Aa-3MO'].diff(periods=1)
        df['CS-A-3MO-diff'] = df['CS-A-3MO'].diff(periods=1)
        df['CS-Baa-3MO-diff'] = df['CS-Baa-3MO'].diff(periods=1)
        df['CS-Aaa-1YR-diff'] = df['CS-Aa-1YR'].diff(periods=1)
        df['CS-Aa-1YR-diff'] = df['CS-Aa-1YR'].diff(periods=1)
        df['CS-A-1YR-diff'] = df['CS-A-1YR'].diff(periods=1)
        df['CS-Baa-1YR-diff'] = df['CS-Baa-1YR'].diff(periods=1)

        df['CS-Aaa-5YR-diff'] = df['CS-Aa-5YR'].diff(periods=1)
        df['CS-Aa-5YR-diff'] = df['CS-Aa-5YR'].diff(periods=1)
        df['CS-A-5YR-diff'] = df['CS-A-5YR'].diff(periods=1)
        df['CS-Baa-5YR-diff'] = df['CS-Baa-5YR'].diff(periods=1)

        # append CS Price diff, although these are not required
        '''
        df['CS-DCF-Aaa-3MO-diff'] = df['CS-DCF-Aaa-3MO'].diff(periods=1)
        df['CS-DCF-Aa-3MO-diff'] = df['CS-DCF-Aa-3MO'].diff(periods=1)
        df['CS-DCF-A-3MO-diff'] = df['CS-DCF-A-3MO'].diff(periods=1)
        df['CS-DCF-Baa-3MO-diff'] = df['CS-DCF-Baa-3MO'].diff(periods=1)

        df['CS-DCF-Aaa-1YR-diff'] = df['CS-DCF-Aaa-1YR'].diff(periods=1)
        df['CS-DCF-Aa-1YR-diff'] = df['CS-DCF-Aa-1YR'].diff(periods=1)
        df['CS-DCF-A-1YR-diff'] = df['CS-DCF-A-1YR'].diff(periods=1)
        df['CS-DCF-Baa-1YR-diff'] = df['CS-DCF-Baa-1YR'].diff(periods=1)

        df['CS-DCF-Aaa-5YR-diff'] = df['CS-DCF-Aaa-5YR'].diff(periods=1)
        df['CS-DCF-Aa-5YR-diff'] = df['CS-DCF-Aa-5YR'].diff(periods=1)
        df['CS-DCF-A-5YR-diff'] = df['CS-DCF-A-5YR'].diff(periods=1)
        df['CS-DCF-Baa-5YR-diff'] = df['CS-DCF-Baa-5YR'].diff(periods=1)
        '''

        # append TB diff
        df['TB-3MO-TY-diff'] = df['TB-3MO-TY'].diff(periods=1)
        df['TB-1YR-TY-diff'] = df['TB-1YR-TY'].diff(periods=1)
        df['TB-5YR-TY-diff'] = df['TB-5YR-TY'].diff(periods=1)
        
        # append Market diff
        df['Market-RMRF-diff'] = df['Market-RMRF'].diff(periods=1)
        df['Market-SP500-diff'] = df['Market-SP500'].diff(periods=1)
        
        # append Econ diff
        df['Econ-UNRATE-diff'] = df['Econ-UNRATE'].diff(periods=1)
        df['Econ-DSPIC96-diff'] = df['Econ-DSPIC96'].diff(periods=1)
        df['Econ-CPIAUCSL-diff'] = df['Econ-CPIAUCSL'].diff(periods=1)
        df['Econ-CPILFESL-diff'] = df['Econ-CPILFESL'].diff(periods=1)
        df['Econ-INDPRO-diff'] = df['Econ-INDPRO'].diff(periods=1)
        df['Econ-PCE-diff'] = df['Econ-PCE'].diff(periods=1)

        # append Market percentage change
        df['Market-SP500-pc-delta'] = (df['Market-SP500'].diff(periods=1) / df['Market-SP500'].shift(1))

        start_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end)

        df = df[start_date:end_date]    # filter records by date

        return df.dropna()

'''
import creditspreadanalysis as csa

if __name__ == "__main__":
    #RunAR()
    #RunDF()
    # csa.RunCommonStats()
    #csa.RunCorrelationPlots()
'''