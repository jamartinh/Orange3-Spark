__author__ = 'jamh'

from Orange.widgets import widget
from pyspark.ml import classification

from orangecontrib.spark.base.spark_ml_estimator import OWSparkEstimator


class OWSparkMLClassification(OWSparkEstimator, widget.OWWidget):
    name = "Classification"
    description = "Classification algorithms"
    icon = "../icons/Category-Classify.svg"

    module = classification
    module_name = 'classification'
    box_text = "Spark Classification Algorithms"
