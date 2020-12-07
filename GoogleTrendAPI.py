import datetime as dt
import os
import pandas as pd

from pytrends.request import TrendReq


class GoogleTrendAPI:
    """
    get Google Trend data. Input: keyword, start date, end date. Output: data frame save to csv
    call method: self.get_data
    """

    def __init__(self):
        self.file_name = 'data/google_trend_data.csv'
        self.keyword = 'bitcoin'
        self.Date_format = '%Y-%m-%d'
        # self.data
        if os.path.isfile(self.file_name): # if file exists
            print(self.file_name, ": Google trend data file exist and will be loaded")  # scaffolding code
            self.data = pd.read_csv(self.file_name, parse_dates=['Date'])  # parsing column 'Date' as a date column
        else:
            self.data = None
            print(self.file_name,": Google trend data file does not exist")  # scaffolding code
        self.pytrend = TrendReq()  # connect to Google

    def get_data(self, start, end):  # the only method that will be called from outside.
        if self.data is None:
            self.load_data(start, end)
            return self.data
        if end > self.data['Date'].max():  # load additional data if the end date is after last date in available data
            print('loading additional data from ', self.data['Date'].max(), 'to, ', end)
            self.load_data(self.data['Date'].max(), end)
        return self.data[((self.data['Date'] >= start) & (self.data['Date'] <= end))]

    def load_data(self, start, end): # self is passed explicitly when define, but implicitly & automatically when called
        # count=0
        while start < end - dt.timedelta(days=30):
            if self.data is None:
                self.data = self.get_py_trend(start, start + dt.timedelta(30)) # return data frame
            self.data = self.merge(self.data, self.get_py_trend(start, start + dt.timedelta(30))) # merging old data
            print('start: ', start, 'end: ', start + dt.timedelta(30))  # 30 days, why the output has 360 days?
            start += dt.timedelta(30)
            # count += 1
            # print('# of calls', count)

        # x = self.data['bitcoin'][2] # test
        # quit()
        if start < end:
            self.data = self.merge(self.data, self.get_py_trend(start, end))
        self.close()

    def get_py_trend(self, start, end):
        date_range = start.strftime(self.Date_format) + ' ' + end.strftime(self.Date_format)
        # string from time, target format is Date_format
        self.pytrend.build_payload(kw_list=[self.keyword], timeframe=date_range)
        # get Google trend data with keyword and everyday inside the date_range
        data_temp = self.pytrend.interest_over_time().reset_index()
        # returns historical, indexed data for when the keyword was searched most as shown on Google Trends'
        # Interest Over Time section
        # reset_index() remove index levels (bring date and bitcoin to the same row)

        if data_temp is None or data_temp.empty:
            return
        df = data_temp[['date', self.keyword]].rename(columns={'date': 'Date'})
        # select the list of column [date , keyword], rename date to Date
        #  pd.set_option('display.max_columns', None)
        #  print(df.iloc[0:5])
        #  quit()
        return df

    def merge(self, df1, df2):  # merge and renormalize
        if df2 is None:
            return df1
        overlap = (set(df1['Date'].unique()) & set(df2['Date'].unique())).pop()
        # return the intersection of two sets of unique dates
        print('overlap',overlap)
        # quit()
        # raise('continue here')
        df1_val = df1[(df1['Date'] == overlap)][self.keyword].sum() #
        df2_val = df2[(df2['Date'] == overlap)][self.keyword].sum()
        df2[self.keyword] = df2[self.keyword] / df2_val * df1_val
        # normalize to df1 values because on overlap dates, the value must be equal
        df = pd.concat([df1, df2], ignore_index=True)
        df = df.drop_duplicates('Date')
        df = df.sort_values(by='Date')
        return df

    def get_current(self):
        """Update the data to current date"""
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
        self.data.to_csv(self.file_name, index=False)  # save to csv file: make-shift database

