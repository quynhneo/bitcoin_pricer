from sklearn.linear_model import LinearRegression
from GenericModel import GenericModel

class LinearRegressionModel(GenericModel):
    """ inherit from GenericModel class. overwrite two class variables, MODEL_NAME and MODEL_CLASS:
    """
    MODEL_NAME = 'model/LinearRegression.mdl'
    MODEL_CLASS = LinearRegression

