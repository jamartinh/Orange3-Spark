__author__ = 'jamh'
from collections import OrderedDict

from Orange.widgets import widget, gui, settings
from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext

from ..utils.gui_utils import GuiParam


class OWSparkContext(widget.OWWidget):
    name = "SparkContext"
    description = "Spark and Hive Contexts"
    icon = "icons/spark.png"
    inputs = []
    outputs = [("SparkContext", SparkContext, widget.Default),
               ("HiveContext", HiveContext, widget.Default)]
    #settingsHandler = settings.DomainContextHandler()

    want_main_area = False
    resizing_enabled = True

    conf = None
    sc = None
    sqlContext = None

    def __init__(self):
        super().__init__()

        # The main label of the Control's GUI.
        #gui.label(self.controlArea, self, "Spark Context")

        # Create parameters Box.
        box = gui.widgetBox(self.controlArea, "Spark Application", addSpace = True)


        self.gui_parameters = OrderedDict()
        self.gui_parameters['spark.app.name'] = GuiParam(parent_widget = box, label = 'spark.app.name', default_value = 'OrangeSpark')
        self.gui_parameters['spark.master'] = GuiParam(parent_widget = box, label = 'spark.master', default_value = 'local[1]')
        self.gui_parameters['spark.executor.memory'] = GuiParam(parent_widget = box, label = 'spark.executor.memory', default_value = '4g')
        self.gui_parameters['spark.driver.memory'] = GuiParam(parent_widget = box, label = 'spark.driver.memory', default_value = '2g')

        action_box = gui.widgetBox(box)
        # Action Button
        self.create_sc_btn = gui.button(action_box, self, label = 'Submit', callback = self.create_context)

    def onDeleteWidget(self):
        if self.sc:
            self.sc.stop()

    def create_context(self):
        self.conf = SparkConf()
        for key, parameter in self.gui_parameters.items():
            self.conf.set(key, parameter.get_value())

        self.sc = SparkContext(conf = self.conf)
        self.sqlContext = HiveContext(self.sc)
        self.send("SparkContext", self.sc)
        self.send("HiveContext", self.sqlContext)
