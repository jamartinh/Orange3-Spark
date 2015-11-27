__author__ = 'jamh'

from Orange.widgets import widget
from pyspark.ml import feature

from orangecontrib.spark.base.spark_ml_transformer import OWSparkTransformer


class OWSparkMLFeature(OWSparkTransformer, widget.OWWidget):
    name = "Feature"
    description = "Features"
    icon = "../icons/FeatureConstructor.svg"

    module = feature
    module_name = 'feature'
    box_text = "Spark Feature Transformers"
