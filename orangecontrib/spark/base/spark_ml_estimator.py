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

    def apply(self):
        method_instance = self.method()
        paramMap = self.build_param_map()
        self.out_model = method_instance.fit(self.in_df, params = paramMap)
        self.send("Model", self.out_model)
