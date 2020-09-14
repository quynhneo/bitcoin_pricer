from sklearn.svm import SVR
from GenericModel import GenericModel

class SVMRegressionModel(GenericModel):
    MODEL_NAME = 'model/SVMRegression.mdl'
    MODEL_CLASS = SVR
    EXTRA_MODEL_ARGS = {'gamma':'scale',  'C':1.0,  'epsilon':0.2}