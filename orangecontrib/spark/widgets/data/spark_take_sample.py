__author__ = 'jamh'
from collections import OrderedDict

import pyspark
from Orange.widgets import widget, gui, settings

from orangecontrib.spark.utils.gui_utils import GuiParam


class OWSparkDFSample(widget.OWWidget):
    priority = 7
    name = "Sample"
    description = "Take a fraction sample of the DataFrame"
    icon = "../icons/DataSampler.svg"

    inputs = [("DataFrame", pyspark.sql.DataFrame, "get_input", widget.Default)]
    outputs = [("DataFrame", pyspark.sql.DataFrame, widget.Default)]
    settingsHandler = settings.DomainContextHandler()

    in_df = None

    def __init__(self):
        super().__init__()
        gui.label(self.controlArea, self, "Sample parameters:")
        # Create parameters Box.

        self.box = gui.widgetBox(self.controlArea, addSpace = True)
        self.gui_parameters = OrderedDict()
        self.gui_parameters['withReplacement'] = GuiParam(parent_widget = self.box, label = 'withReplacement', default_value = 'False')
        self.gui_parameters['fraction'] = GuiParam(parent_widget = self.box, label = 'fraction', default_value = '0.5')
        self.gui_parameters['seed'] = GuiParam(parent_widget = self.box, label = 'seed', default_value = '1')

        self.action_box = gui.widgetBox(self.box)
        # Action Button
        self.create_sc_btn = gui.button(self.action_box, self, label = 'Apply', callback = self.apply)

    def get_input(self, obj = None):
        self.in_df = obj

    def apply(self):
        if self.in_df:
            withReplacement = self.gui_parameters['withReplacement'].get_usable_value()
            fraction = self.gui_parameters['fraction'].get_usable_value()
            seed = self.gui_parameters['seed'].get_usable_value()
            self.send("DataFrame", self.in_df.sample(withReplacement, fraction, seed))
