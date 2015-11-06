__author__ = 'jamh'

from Orange.data import Table
from PyQt4.QtGui import QSizePolicy
from Orange.widgets import widget, gui
from orangecontrib.spark.utils.bdutils import pandas_to_orange
import pandas
from Orange.widgets import widget, gui, settings
from pyspark import SparkConf, SparkContext
import pyspark


class OWOrangeToPandas(widget.OWWidget):
    name = "Spark to Pandas"
    description = "Convert Spark dataframe to Pandas"
    icon = "icons/spark.ico"

    inputs = [("Sparkdf", pyspark.sql.DataFrame, "get_input", widget.Default)]
    outputs = [("Dataframe", pandas.DataFrame, widget.Dynamic)]
    settingsHandler = settings.DomainContextHandler()

    NOTHING = "Nothing on input"

    def __init__(self):
        super().__init__()
        self.obj_type = self.NOTHING
        gui.label(self.controlArea, self, "Spark->Pandas:")
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

    def get_input(self, obj):
        self.obj_type = self.NOTHING if obj is None else type(obj).__name__

        self.send("Table", obj.toPandas())
