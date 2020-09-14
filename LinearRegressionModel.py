from sklearn.linear_model import LinearRegression
from GenericModel import GenericModel

class LinearRegressionModel(GenericModel):
    MODEL_NAME = 'model/LinearRegression.mdl'
    MODEL_CLASS = LinearRegression