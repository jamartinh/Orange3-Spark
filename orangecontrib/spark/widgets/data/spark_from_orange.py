__author__ = 'jamh'

import pyspark
from Orange.data import Table
from Orange.widgets import widget, gui, settings

from orangecontrib.spark.base.shared_spark_context import SharedSparkContext
from orangecontrib.spark.utils.data_utils import orange_to_pandas


class OWSparkFromOrange(SharedSparkContext, widget.OWWidget):
    priority = 7
    name = "from Orange"
    description = "Convert Orange Table to Spark DataFrame"
    icon = "../icons/spark.png"

    inputs = [("Table", Table, "get_input", widget.Default)]
    outputs = [("DataFrame", pyspark.sql.DataFrame, widget.Dynamic)]
    settingsHandler = settings.DomainContextHandler()

    auto_commit = settings.Setting(True)

    def __init__(self):
        super().__init__()
        gui.label(self.controlArea, self, "From Oranges:")

    def get_input(self, obj):
        self.send("DataFrame", self.hc.createDataFrame(orange_to_pandas(obj)))
