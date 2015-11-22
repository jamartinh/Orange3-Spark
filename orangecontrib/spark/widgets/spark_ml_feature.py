__author__ = 'jamh'

from Orange.widgets import widget
from pyspark.ml import feature

from ..base.spark_ml_transformer import OWSparkTransformer


class OWSparkMLFeature(OWSparkTransformer, widget.OWWidget):
    name = "Feature"
    description = "Features"
    icon = "icons/spark.png"

    module = feature
    module_name = 'feature'
    box_text = "Spark Feature Transformers"
