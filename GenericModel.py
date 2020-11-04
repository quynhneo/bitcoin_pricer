import os
from datetime import datetime, timedelta
# from sklearn.externals\
import joblib
import pandas as pd

from GoogleTrendAPI import GoogleTrendAPI
from FinanceAPI import FinanceAPI


class GenericModel:
    """GenericModel calls finance data and google trend TO GET DATA,
    and provides methods to train and make predictions"""
    MODEL_NAME = ''
    MODEL_CLASS = None
    EXTRA_MODEL_ARGS = {}

    def __init__(self, finance_api=None, google_trend_api=None):
        """constructor
        """
        self.finance_api = finance_api if finance_api is not None else FinanceAPI()   # initiate finance api if not
        # already exist
        self.google_trend_api = google_trend_api if google_trend_api is not None else GoogleTrendAPI()
        # initiate Google api if not already exist
        if os.path.isfile(self.MODEL_NAME):  # Return True if 'MODEL_NAME' is an existing regular file
            self.model = joblib.load(self.MODEL_NAME) # load the model from file
            print(self.MODEL_NAME,'model file exists and loaded')  # scaffolding code
        else:  # call an instance of model class (from scikit-learn)
            self.model = self.MODEL_CLASS(**self.EXTRA_MODEL_ARGS)  #

    def train(self, start, end):
        """ train
        INPUT: model object, start date, end date
        OUTPUT: return None, fit the model to data
        """
        google_trend_df = self.google_trend_api.get_data(start, end)
        finance_df = self.finance_api.get_data(start, end)
        df = finance_df.merge(google_trend_df, on=['Date'])
        df = df.dropna()
        X = df[['^GSPC', '^VIX', 'Volume', 'bitcoin']]  # input
        y = df['BTC-USD'] #
        self.model.fit(X, y)  # fit the data to the model

    def predict(self, attributes):
        df = pd.DataFrame([attributes], columns=['^GSPC', '^VIX', 'Volume', 'bitcoin'])
        return self.model.predict(df)

    def score(self):
        google_trend_df = self.google_trend_api.get_data(datetime.today() - timedelta(days=30), datetime.today())
        finance_df = self.finance_api.get_data(datetime.today() - timedelta(days=30), datetime.today())
        df = finance_df.merge(google_trend_df, on=['Date'])
        df = df.dropna()
        X = df[['^GSPC', '^VIX', 'Volume', 'bitcoin']]
        y = df['BTC-USD']
        return self.model.score(X, y)

    def save(self): # save model object to file, path given by MODEL_NAME
        joblib.dump(self.model, self.MODEL_NAME)
