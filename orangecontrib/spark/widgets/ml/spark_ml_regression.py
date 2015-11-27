__author__ = 'jamh'

from Orange.widgets import widget
from pyspark.ml import regression

from orangecontrib.spark.base.spark_ml_estimator import OWSparkEstimator


class OWSparkMLRegression(OWSparkEstimator, widget.OWWidget):
    priority = 3
    name = "Regression"
    description = "regression algorithms"
    icon = "../icons/Regression.svg"

    module = regression
    module_name = 'regression'
    box_text = "Spark Regression Algorithms"
