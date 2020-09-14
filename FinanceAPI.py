import datetime
import pandas_datareader.data as web
import pandas as pd

class FinanceAPI:

    def __init__(self):
        self.file_name = 'data/finance_data.csv'
        self.data = pd.read_csv((self.file_name), parse_dates=['Date'])

    def get_data(self, start, end):
        if end.date() > self.data['Date'].max().date():
            self.load_data(self.data['Date'].max() + datetime.timedelta(days=1), end)
        return self.data[((self.data['Date'] >= start) & (self.data['Date'] <= end))]

    def load_data(self, start, end):
        df = web.DataReader(['^GSPC', '^VIX'], 'yahoo', start, end)
        df = df['Adj Close'].reset_index()
        df_btc = web.DataReader('BTC-USD', 'yahoo', start, end)
        df_btc_volume = df_btc['Volume'].reset_index()
        df_btc_price = df_btc['Adj Close'].reset_index()
        df = df.merge(df_btc_volume, how='outer', on=['Date']).merge(df_btc_price, how='outer', on=['Date']).rename(columns={'Adj Close': 'BTC-USD'})
        df = df.sort_values(by='Date')
        for col in df.columns:
            df[col] = df[col].ffill()

        self.data = pd.concat([self.data, df], ignore_index=True)

    def get_current(self):
        end = datetime.datetime.today()
        start = end - datetime.timedelta(days=5)
        self.data = self.data[(self.data['Date'] < start)]
        self.load_data(start, end)
        return self.data.loc[(self.data['Date'] == self.data['Date'].max())].to_dict(orient='records')[0]

    def close(self):
        for col in self.data:
            if col.startswith('Unnamed'):
                self.data.drop(columns=[col])

        self.data.to_csv((self.file_name), index=False)