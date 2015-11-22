__author__ = 'jamh'

from Orange.widgets import widget
from pyspark.ml import classification

from ..base.spark_ml_estimator import OWSparkEstimator


class OWSparkMLClassification(OWSparkEstimator, widget.OWWidget):
    name = "Classification"
    description = "Classification algorithms"
    icon = "icons/spark.png"

    module = classification
    module_name = 'classification'
    box_text = "Spark Classification Algorithms"
