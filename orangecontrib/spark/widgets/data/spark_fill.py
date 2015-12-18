__author__ = 'jamh'
from collections import OrderedDict

import pyspark
from Orange.widgets import widget, gui, settings
from Orange.widgets.settings import Setting
from PyQt4 import QtGui

from orangecontrib.spark.utils.gui_utils import GuiParam
from orangecontrib.spark.utils.spark_api_utils import get_dataframe_function_info


class OWSparkFillNa(widget.OWWidget):
    priority = 4
    name = "FillNa"
    description = "Replace null values"
    icon = "../icons/Impute.svg"

    inputs = [("DataFrame", pyspark.sql.DataFrame, "get_input", widget.Default)]
    outputs = [("DataFrame", pyspark.sql.DataFrame, widget.Default)]
    settingsHandler = settings.DomainContextHandler()

    in_df = None
    want_main_area = False
    resizing_enabled = True
    saved_gui_params = Setting(OrderedDict())

    def __init__(self):
        super().__init__()

        self.main_box = gui.widgetBox(self.controlArea, orientation = 'horizontal', addSpace = True)
        self.box = gui.widgetBox(self.main_box, 'Parameters:', addSpace = True)
        self.help_box = gui.widgetBox(self.main_box, 'Documentation', addSpace = True)

        self.gui_parameters = OrderedDict()

        # Create method label doc.
        self.method_info_label = QtGui.QTextEdit('', self.help_box)
        self.method_info_label.setAcceptRichText(True)
        self.method_info_label.setReadOnly(True)
        self.method_info_label.autoFormatting()
        self.method_info_label.setText(get_dataframe_function_info('fillna'))
        self.help_box.layout().addWidget(self.method_info_label)

        # Create parameters Box.
        self.gui_parameters = OrderedDict()
        default_value = self.saved_gui_params.get('value', '0')
        self.gui_parameters['value'] = GuiParam(parent_widget = self.box, label = 'value', default_value = default_value)
        default_value = self.saved_gui_params.get('subset', 'None')
        self.gui_parameters['subset'] = GuiParam(parent_widget = self.box, label = 'fraction', default_value = 'None')

        self.action_box = gui.widgetBox(self.box)
        # Action Button
        self.create_sc_btn = gui.button(self.action_box, self, label = 'Apply', callback = self.apply)

    def get_input(self, obj = None):
        self.in_df = obj

    def apply(self):
        if self.in_df:
            value = self.gui_parameters['value'].get_usable_value()
            subset = self.gui_parameters['subset'].get_usable_value()
            self.send("DataFrame", self.in_df.fill(value, subset))
            self.update_saved_gui_parameters()
            self.hide()

    def update_saved_gui_parameters(self):
        for k in self.gui_parameters:
            self.saved_gui_params[k] = self.gui_parameters[k].get_value()
