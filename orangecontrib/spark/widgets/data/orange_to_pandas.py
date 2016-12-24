__author__ = 'jamh'

import pandas
from Orange.data import Table
from Orange.widgets import widget, gui, settings

from orangecontrib.spark.utils.data_utils import orange_to_pandas


class OWOrangeToPandas(widget.OWWidget):
    name = "to Pandas"
    description = "Convert Orange Table to Pandas DataFrame"
    icon = "../icons/orange-canvas.svg"

    inputs = [("Table", Table, "get_input", widget.Default)]
    outputs = [("Pandas", pandas.DataFrame, widget.Dynamic)]
    settingsHandler = settings.DomainContextHandler()

    def __init__(self):
        super().__init__()
        gui.label(self.controlArea, self, "to pandas:")

    def get_input(self, obj):
        self.send("Pandas", orange_to_pandas(obj))
