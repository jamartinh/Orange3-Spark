__author__ = 'jamh'
from Orange.widgets import widget, gui, settings
from PyQt4 import QtGui
from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
from ..utils.gui_utils import dict_to_text_widgets
from collections import OrderedDict


class OWSparkContext(widget.OWWidget):
    name = "SparkContext"
    description = "Spark and Hive Contexts"
    icon = "icons/spark.png"
    inputs = []
    outputs = [("SparkContext", SparkContext, widget.Default),
               ("HiveContext", HiveContext, widget.Default)]
    settingsHandler = settings.DomainContextHandler()

    want_main_area = False
    resizing_enabled = True

    conf = None
    sc = None
    sqlContext = None

    def __init__(self):
        super().__init__()
        parameters_dict = OrderedDict()
        parameters_dict['spark.app.name'] = ['spark.app.name', 'OrangeSpark']
        parameters_dict['spark.master'] = ['spark.master', 'local']
        parameters_dict['spark.executor.memory'] = ['spark.executor.memory', '8g']
        parameters_dict['spark.driver.memory'] = ["spark.driver.memory", "2g"]

        gui.label(self.controlArea, self, "Spark Context")

        vbox = gui.widgetBox(self.controlArea, "Spark Application", addSpace = True)
        box = gui.widgetBox(vbox)

        self.params = dict_to_text_widgets(parameters_dict, box)

        self.create__sc_btn = gui.button(
            box, self, label = 'Submit', callback = self.create_context)

    def onDeleteWidget(self):
        if self.sc:
            self.sc.stop()

    def create_context(self):
        self.conf = SparkConf()
        for key, text_widget in self.params.items():
            self.conf.set(key, text_widget.text())

        self.sc = SparkContext(conf = self.conf)
        self.sqlContext = HiveContext(self.sc)
        self.send("SparkContext", self.sc)
        self.send("HiveContext", self.sqlContext)
