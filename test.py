import datetime as dt
# import pandas as pd
# from pytrends.request import TrendReq
from LinearRegressionModel import LinearRegressionModel
from LassoRegressionModel import LassoRegressionModel


def main():
    # CHOOSE A MODEL
    model = LinearRegressionModel()
    # model = LassoRegressionModel()
    print('started model')
    model.train(dt.datetime.today() - dt.timedelta(days=90), dt.datetime.today())  # (start date, end date)
    print('finish training')
    model.save()

    # INPUT VALUES FOR ['^GSPC', '^VIX', 'Volume', 'bitcoin']
    x = [3319.47, 25.83, 22825594880, 65]
    print('Given ^GSPC = ', x[0], ', ^VIX = ', x[1], ',Volume = ', x[2], ',Google Trend bitcoin =', x[3])
    print('Predicted price of Bitcoin:', model.predict(x))
    print('R^2 score: ', model.score())

main()
