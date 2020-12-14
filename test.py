import datetime as dt
# import pandas as pd
# from pytrends.request import TrendReq
from LinearRegressionModel import LinearRegressionModel
from LassoRegressionModel import LassoRegressionModel


def main():
    model = LinearRegressionModel() # Initiate a model
    # choose the time range of data:
    start_date, end_date = dt.datetime.today() - dt.timedelta(days=365), dt.datetime.today()
    model.plot_data(start_date,end_date)
    model.train(start_date, end_date)  # train the model on data
    print('finish training')
    model.save()

    # INPUT VALUES FOR ['^GSPC', '^VIX', 'Volume', 'bitcoin']
    x = [3319.47, 25.83, 22825594880, 65]
    print('Given ^GSPC = ', x[0], ', ^VIX = ', x[1], ',Volume = ', x[2], ',Google Trend bitcoin =', x[3])
    print('Predicted price of Bitcoin:', model.predict(x))
    print('R^2 score: ', model.score())

main()
