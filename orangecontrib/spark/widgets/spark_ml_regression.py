__author__ = 'jamh'

from Orange.widgets import widget
from pyspark.ml import regression

from ..base.spark_ml_estimator import OWSparkEstimator


class OWSparkMLRegression(OWSparkEstimator, widget.OWWidget):
    name = "Regression"
    description = "regression algorithms"
    icon = "icons/spark.png"

    module = regression
    module_name = 'regression'
    box_text = "Spark Regression Algorithms"
