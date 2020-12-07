from sklearn.linear_model import Lasso
from GenericModel import GenericModel


class LassoRegressionModel(GenericModel):
    MODEL_CLASS = Lasso
    MODEL_NAME = 'model/lasso.mdl'
    EXTRA_MODEL_ARGS = {'alpha': 0.1}
