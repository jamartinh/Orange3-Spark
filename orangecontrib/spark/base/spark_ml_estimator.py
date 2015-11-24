__author__ = 'jamh'

from Orange.widgets import widget
from pyspark.ml import Model

from .spark_ml_transformer import OWSparkTransformer
from ..utils.ml_api_utils import get_estimators


class OWSparkEstimator(OWSparkTransformer):
    name = "Estimator"
    description = "An Estimator of the Spark ml api"
    icon = "icons/spark.png"
    out_model = None
    outputs = [("Model", Model, widget.Dynamic)]

    get_modules = get_estimators

    def fit(self):
        self.out_model = self.method.fit(self.in_df)
        self.send("Model", self.out_model)
