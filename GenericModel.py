import os
from datetime import datetime, timedelta
# from sklearn.externals\
import joblib
import pandas as pd

from Data import Data

class GenericModel:
    """Abstract class
    Class variables MODEL_NAME, MODEL_CLASS, EXTRA_MODEL_ARGS are to be overwritten by child class
    Class methods:
    __init__:  model
    train: train the model given by MODEL_CLASS or saved in MODEL_NAME
    predict: predict bitcoin price
    score: calculate R^2 score, using data from recent dates as test data
    save: save model to MODEL_NAME
    """
    MODEL_NAME = ''  # file path of saved model. to be be overwritten by child class
    MODEL_CLASS = None  # to be overwritten by child class
    EXTRA_MODEL_ARGS = {}  # to be overwritten by child class

    def __init__(self):
        """Constructor: initiate model by loading or new instance """
        self.data = Data()
        if os.path.isfile(self.MODEL_NAME):  # Return True if 'MODEL_NAME' is an existing regular file
            self.model = joblib.load(self.MODEL_NAME)  # load the model from file
            print(self.MODEL_NAME, 'model file exists and loaded')  # scaffolding code
        else:  # call an instance of model class (from scikit-learn)
            self.model = self.MODEL_CLASS(**self.EXTRA_MODEL_ARGS)  #

    def train(self, start, end):
        """ Train the model with data
        INPUT: model object, start date, end date
        OUTPUT: return None, fit the model to data
        """
        X, y, _, _ = self.data.gather_data(start, end)
        self.model.fit(X, y)  # fit the data to the model

    def predict(self, attributes):
        """Predict using the linear model
        INPUT: finance data '^GSPC', '^VIX', 'Volume' and Google Trend data for 'bitcoin'
        OUTPUT: bitcoin price
        """
        df = pd.DataFrame([attributes], columns=['^GSPC', '^VIX', 'Volume', 'bitcoin'])
        return self.model.predict(df)

    def score(self, start, end):
        """Return the coefficient of determination R^2 of the prediction
        using data from recent dates as test data
        R = 1 means prediction = data (ideal case), R = 0 means prediction always = mean(true)"""

        _, _, X, y = self.data.gather_data(start, end)  # get the test data
        return self.model.score(X, y)

    def save(self):  # save model object to file, path given by MODEL_NAME
        joblib.dump(self.model, self.MODEL_NAME)
