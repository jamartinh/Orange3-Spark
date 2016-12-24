__author__ = 'jamh'
from Orange.data import Table
from PyQt4.QtGui import QSizePolicy
from Orange.widgets import widget, gui
from orangecontrib.spark.utils.data_utils import pandas_to_orange
import pandas
from Orange.widgets import widget, gui, settings
from pyspark import SparkConf, SparkContext
import pyspark


class OWSparkToOrange(widget.OWWidget):
    priority = 9
    name = "to Orange"
    description = "Convert Spark dataframe to Orange Table"
    icon = "../icons/spark.png"

    inputs = [("Sparkdf", pyspark.sql.DataFrame, "get_input", widget.Default)]
    outputs = [("Table", Table, widget.Dynamic)]
    settingsHandler = settings.DomainContextHandler()

    NOTHING = "Nothing on input"

    def __init__(self):
        super().__init__()

        gui.label(self.controlArea, self, "Spark->Orange:")
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

    def get_input(self, obj):
        df = obj.toPandas()
        self.send("Table", pandas_to_orange(df))
