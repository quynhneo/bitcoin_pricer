from GoogleTrendAPI import GoogleTrendAPI
from FinanceAPI import FinanceAPI
import matplotlib.pyplot as plt


class Data:
    def __init__(self, finance_api=None, google_trend_api=None):
        """Constructor: Initiate finance_api and google_trend_api
        """
        self.finance_api = finance_api if finance_api is not None else FinanceAPI()  # initiate finance api if not
        # provided (default)
        self.google_trend_api = google_trend_api if google_trend_api is not None else GoogleTrendAPI()
        # initiate Google api if not provided (default)

    def gather_data(self, start, end):
        """Gather the data from the Google and Yahoo APIs
        return a merged data frame
        """
        google_trend_df = self.google_trend_api.get_data(start, end)
        # shape (days,2), columns  = Date , bitcoin
        finance_df = self.finance_api.get_data(start, end)
        # shape (days,5), columns  = Date , ^GSPC , ^VIX, Volume , BTC-USD
        df = finance_df.merge(google_trend_df, on=['Date'])
        df = df.dropna()
        return df

    def train_data(self, start, end):
        """train data, first 2/3 of the data range"""
        df = self.gather_data(start, end)
        df_train = df[:int(df.shape[0] * 2 / 3)]
        X_train = df_train[['^GSPC', '^VIX', 'Volume', 'bitcoin']]  # input
        y_train = df_train['BTC-USD']  #

        return (X_train, y_train)

    def test_data(self, start, end):
        """test data, last 1/3 of the data range"""
        df = self.gather_data(start, end)
        df_test = df[int(df.shape[0] * 2 / 3):]
        X_test = df_test[['^GSPC', '^VIX', 'Volume', 'bitcoin']]  # input
        y_test = df_test['BTC-USD']  #

        return (X_test, y_test)

    def plot_data(self, start, end):
        """Plot the train data"""
        X, y = self.train_data(start, end)  # get the train data
        # plotting
        f = plt.figure(figsize=(10, 10))
        ax = f.add_subplot(2, 2, 1)
        ax.plot(X.index, X[['^GSPC']], 'o-')
        ax.set_xlabel('days since ' + str(start.year) + '-' + str(start.month) + '-' + str(start.day))
        ax.set_ylabel('GSPC')
        ax = f.add_subplot(2, 2, 2)
        ax.plot(X.index, X[['^VIX']], 'o-')
        ax.set_xlabel('days since ' + str(start.year) + '-' + str(start.month) + '-' + str(start.day))
        ax.set_ylabel('VIX')
        ax = f.add_subplot(2, 2, 3)
        ax.plot(X.index, X[['Volume']], 'o-')
        ax.set_xlabel('days since ' + str(start.year) + '-' + str(start.month) + '-' + str(start.day))
        ax.set_ylabel('Volume')
        ax = f.add_subplot(2, 2, 4)
        ax.plot(X.index, X[['bitcoin']], 'o-')
        ax.set_xlabel('days since ' + str(start.year) + '-' + str(start.month) + '-' + str(start.day))
        ax.set_ylabel('Google Trend for \'bitcoin\' ')

        f2 = plt.figure(figsize=(5, 5))
        plt.plot(y.index, y, 'o-')
