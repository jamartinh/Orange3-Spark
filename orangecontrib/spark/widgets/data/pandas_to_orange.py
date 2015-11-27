__author__ = 'jamh'
from Orange.data import Table
import pandas
from Orange.widgets import widget, gui, settings

from orangecontrib.spark.utils.bdutils import pandas_to_orange


class OWPandasToOrange(widget.OWWidget):
    name = "from Pandas"
    description = "Convert Pandas DataFrame to Orange Table"
    icon = "../icons/orange.ico"
    inputs = [("Pandas", pandas.DataFrame, "get_input", widget.Default)]
    outputs = [("Table", Table, widget.Dynamic)]
    settingsHandler = settings.DomainContextHandler()

    def __init__(self):
        super().__init__()
        gui.label(self.controlArea, self, "from pandas:")

    def get_input(self, obj):
        self.send("Table", pandas_to_orange(obj))
