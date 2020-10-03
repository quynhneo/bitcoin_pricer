import datetime as dt
# import pandas as pd
# from pytrends.request import TrendReq
from LinearRegressionModel import LinearRegressionModel


def main():
    model = LinearRegressionModel()
    print('started model')
    model.train(dt.datetime.today() - dt.timedelta(days=360), dt.datetime.today())
    print('finishtraining')
    model.save()
    print(model.predict([3319.47, 25.83,22825594880, 65]))
    print(model.score())

main()