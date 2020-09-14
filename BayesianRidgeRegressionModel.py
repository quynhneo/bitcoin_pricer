from sklearn.linear_model import BayesianRidge
from GenericModel import GenericModel

class BayesianRidgeRegressionModel(GenericModel):
    MODEL_CLASS = BayesianRidge
    MODEL_NAME = 'model/bayesian_ridge.mdl'