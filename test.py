import datetime as dt
# import pandas as pd
# from pytrends.request import TrendReq
from LinearRegressionModel import LinearRegressionModel
from LassoRegressionModel import LassoRegressionModel
from Data import Data

model = LinearRegressionModel() # Initiate a model
# choose the time range of data:
start_date, end_date = dt.datetime.today() - dt.timedelta(days=90), dt.datetime.today()
data = Data()
data.plot_data(start_date,end_date)
X,y = data.train_data(start_date,end_date)
model.train(X,y)  # train the model on data
# print('finish training')
# model.save()

# # INPUT VALUES FOR ['^GSPC', '^VIX', 'Volume', 'bitcoin']
xtest = [3319.47, 25.83, 22825594880, 65]
print('Given ^GSPC = ', xtest[0], ', ^VIX = ', xtest[1], ',Volume = ', xtest[2], ',Google Trend bitcoin =', xtest[3])
print('Predicted price of Bitcoin:', model.predict(xtest))
X_,y_ = data.test_data(start_date,end_date)
print('R^2 score: ', model.score(X_,y_))

