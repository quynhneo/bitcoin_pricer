from sklearn.linear_model import Ridge
from GenericModel import GenericModel

class RidgeRegressionMode(GenericModel):
    MODEL_CLASS = Ridge
    MODEL_NAME = 'model/ridge.mdl'
    EXTRA_MODEL_ARGS = {'alpha': 0.5}