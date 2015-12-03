__author__ = 'jamh'

import pandas
import pyspark
from Orange.widgets import widget, gui, settings
from PyQt4.QtGui import QSizePolicy

from orangecontrib.spark.base.shared_spark_context import SharedSparkContext


class OWSparkToPandas(SharedSparkContext, widget.OWWidget):
    priority = 6
    name = "from Pandas"
    description = "Convert Pandas dataframe to Spark DataFrame."
    icon = "../icons/spark.png"

    inputs = [("DataFrame", pandas.DataFrame, "get_input", widget.Default)]
    outputs = [("DataFrame", pyspark.sql.DataFrame, widget.Dynamic)]
    settingsHandler = settings.DomainContextHandler()

    def __init__(self):
        super().__init__()
        gui.label(self.controlArea, self, "Pandas->Spark:")
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

    def get_input(self, obj):
        self.send("DataFrame", self.hc.createDataFrame(obj))
