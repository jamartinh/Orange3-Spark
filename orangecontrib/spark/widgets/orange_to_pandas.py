__author__ = 'jamh'

import pandas
from Orange.data import Table
from Orange.widgets import widget, gui, settings
from PyQt4.QtGui import QSizePolicy

from ..utils.bdutils import orange_to_pandas


class OWOrangeToPandas(widget.OWWidget):
    name = "To Pandas"
    description = "Convert Orange Table to Pandas DataFrame"
    icon = "icons/Hub.svg"

    inputs = [("Table", Table, "get_input", widget.Default)]
    outputs = [("Pandas", pandas.DataFrame, widget.Dynamic)]
    settingsHandler = settings.DomainContextHandler()

    variable_state = settings.ContextSetting({})

    optimization = settings.Setting(0)

    color_index = settings.ContextSetting(0)
    shape_index = settings.ContextSetting(0)
    size_index = settings.ContextSetting(0)

    point_size = settings.Setting(10)
    alpha_value = settings.Setting(255)
    jitter_value = settings.Setting(0)
    hide_radius = settings.Setting(0)

    auto_commit = settings.Setting(True)

    NOTHING = "Nothing on input"

    def __init__(self):
        super().__init__()
        self.obj_type = self.NOTHING
        gui.label(self.controlArea, self, "to pandas:")
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

    def get_input(self, obj):
        self.obj_type = self.NOTHING if obj is None else type(obj).__name__
        self.send("Pandas", orange_to_pandas(obj))
