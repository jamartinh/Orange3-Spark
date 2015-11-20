__author__ = 'jamh'

from Orange.widgets import gui
from pyspark.ml import feature

from .spark_ml_transformer import OWSparkTransformer


class OWSparkMLFeature(OWSparkTransformer):
    name = "Feature"
    description = "Features"
    icon = "icons/spark.png"

    module = feature
    module_name = 'feature'
    box_text = "Spark Features"


