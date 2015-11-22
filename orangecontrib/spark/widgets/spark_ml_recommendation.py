__author__ = 'jamh'

from Orange.widgets import widget
from pyspark.ml import recommendation

from ..base.spark_ml_estimator import OWSparkEstimator


class OWSparkMLClustering(OWSparkEstimator, widget.OWWidget):
    name = "Recommendation"
    description = "recommendation algorithms"
    icon = "icons/spark.png"

    module = recommendation
    module_name = 'recommendation'
    box_text = "Spark Recommendation Algorithms"
