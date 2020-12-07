import datetime
import os

import pandas as pd
import pandas_datareader.data as web


class FinanceAPI:

    def __init__(self):
        self.file_name = 'data/finance_data.csv'
        if os.path.isfile(self.file_name):
            print(self.file_name, 'finance data file exists and will be loaded')
            self.data = pd.read_csv(self.file_name, parse_dates=['Date'])
        else:
            self.data = None
            print(self.file_name, ": finance data file does not exist")  # scaffolding code

    def get_data(self, start, end):  # the only function that's called from outside
        if self.data is None:
            self.load_data(start, end)
            return self.data
        if end.date() > self.data['Date'].max().date():
            print('loading additional data from ', self.data['Date'].max().date(), 'to, ', end.date())
            self.load_data(self.data['Date'].max() + datetime.timedelta(days=1), end)
        return self.data[((self.data['Date'] >= start) & (self.data['Date'] <= end))]

    def load_data(self, start, end):
        """Load the data from web from start to end day and do some cleaning"""
        df = web.DataReader(['^GSPC', '^VIX'], 'yahoo', start, end)  # shape ( days ,12)
        df = df['Adj Close'].reset_index()  # making Date a col, new shape ( days ,3), columns = Date, ^GSPC, ^VIX

        df_btc = web.DataReader('BTC-USD', 'yahoo', start, end)  # shape (days, 6)
        # pd.set_option('display.max_columns', None)
        # print(df_btc.iloc[0:5])
        # quit()
        df_btc_volume = df_btc['Volume'].reset_index()  # shape (days, 2), columns = Date, Volume
        df_btc_price = df_btc['Adj Close'].reset_index()  # shape (days, 2), columns = Date, Adj Close (close price)

        df = df.merge(df_btc_volume, how='outer', on=['Date']).merge(df_btc_price, how='outer', on=['Date']).rename(
            columns={'Adj Close': 'BTC-USD'})
        # shape (days,5), columns  = Date , ^GSPC , ^VIX, Volume , BTC-USD

        df = df.sort_values(by='Date')
        for col in df.columns:
            df[col] = df[col].ffill()  # fill NaN by propagating non-null values forward in time
        if self.data is None:
            self.data = df
        else:
            self.data = pd.concat([self.data, df], ignore_index=True)  # concatenate
        self.close()  # save to file

    def get_current(self):
        """Update the data to current date"""
        end = datetime.datetime.today()
        start = end - datetime.timedelta(days=5)
        self.data = self.data[(self.data['Date'] < start)]
        self.load_data(start, end)
        return self.data.loc[(self.data['Date'] == self.data['Date'].max())].to_dict(orient='records')[0]

    def close(self):
        for col in self.data:
            if col.startswith('Unnamed'):
                self.data.drop(columns=[col])
        self.data.to_csv(self.file_name, index=False)  # save to csv file: make-shift database
