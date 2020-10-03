import datetime as dt
import os
import pandas as pd

from pytrends.request import TrendReq


class GoogleTrendAPI:

    def __init__(self):
        self.file_name = 'data/google_trend_data.csv'
        self.keyword = 'bitcoin'
        self.Date_format = '%Y-%m-%d'
        if os.path.isfile(self.file_name):
            self.data = pd.read_csv(self.file_name, parse_dates=['Date'])
        else:
            self.data = None
        self.pytrend = TrendReq()

    def get_data(self, start, end):
        if self.data is None:
            self.load_data(start, end)
            return self.data
        if end > self.data['Date'].max():
            self.load_data(self.data['Date'].max(), end)
        return self.data[((self.data['Date'] >= start) & (self.data['Date'] <= end))]

    def load_data(self, start, end):
        while start < end - dt.timedelta(days=30):
            if self.data is None:
                self.data = self.get_py_trend(start, start + dt.timedelta(30))
            self.data = self.merge(self.data, self.get_py_trend(start, start + dt.timedelta(30)))
            start += dt.timedelta(30)

        if start < end:
            self.data = self.merge(self.data, self.get_py_trend(start, end))

    def get_py_trend(self, start, end):
        date_range = start.strftime(self.Date_format) + ' ' + end.strftime(self.Date_format)
        self.pytrend.build_payload(kw_list=[self.keyword], timeframe=date_range)
        data = self.pytrend.interest_over_time().reset_index()
        if data is None or data.empty:
            return
        df = data[['date', self.keyword]].rename(columns={'date': 'Date'})
        return df

    def merge(self, df1, df2):
        if df2 is None:
            return df1
        overlap = (set(df1['Date'].unique()) & set(df2['Date'].unique())).pop()
        df1_val = df1[(df1['Date'] == overlap)][self.keyword].sum()
        df2_val = df2[(df2['Date'] == overlap)][self.keyword].sum()
        df2[self.keyword] = df2[self.keyword] / df2_val * df1_val
        df = pd.concat([df1, df2], ignore_index=True)
        df = df.drop_duplicates('Date')
        df = df.sort_values(by='Date')
        return df

    def get_current(self):
        date_max = self.data['Date'].max()
        if date_max < dt.datetime.today():
            df = self.get_py_trend(date_max, dt.datetime.today())
            if df is not None:
                if not df.empty:
                    self.data = self.merge(self.data, df)
        return self.data.loc[(self.data['Date'] == self.data['Date'].max())].to_dict(orient='records')[0]

    def close(self):
        for col in self.data:
            if col.startswith('Unnamed'):
                self.data.drop(columns=[col])

        self.data.to_csv(self.file_name, index=False)
