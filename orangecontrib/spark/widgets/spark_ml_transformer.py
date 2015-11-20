__author__ = 'jamh'
from collections import OrderedDict

import pyspark
from Orange.widgets import widget, gui, settings
from PyQt4 import QtGui
from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext

from ..utils.gui_utils import GuiParam
from ..utils.ml_api_utils import get_transformers, get_estimators, get_models, get_object_info, get_module_info


class OWSparkTransformer(widget.OWWidget):
    #widget_id = None
    name = "Transformer"
    description = "A Transformer of the Spark ml api"
    icon = "icons/spark.png"
    inputs = [("DataFrame", pyspark.sql.DataFrame, "get_input", widget.Default)]
    outputs = [("DataFrame", pyspark.sql.DataFrame, widget.Dynamic),
               ("SparkContext", pyspark.SparkContext, widget.Default),
               ("HiveContext", pyspark.sql.HiveContext, widget.Default)
               ]
    settingsHandler = settings.DomainContextHandler()

    want_main_area = False
    resizing_enabled = True

    conf = None
    sc = None
    hc = None
    in_df = None
    out_df = None
    obj_type = None
    module = None
    module_name = None
    module_info = None
    box_text = "Spark Application"

    def __init__(self):
        super().__init__()
        #gui.label(self.controlArea, self, "pyspark.ml")
        self.module_info = get_module_info(self.module)

        # Create parameters Box.
        self.box = gui.widgetBox(self.controlArea, self.box_text, addSpace = True)

        # Create module label doc.
        self.module_info_label = QtGui.QLabel(self.module_info, self.box)
        self.box.layout().addWidget(self.module_info_label)

        self.gui_parameters = OrderedDict()
        # Create place for selecting the method
        self.transformers = get_transformers(self.module)
        self.models = get_models(self.module)
        self.estimators = get_estimators(self.module)
        method_names = [t for t in self.transformers]
        self.gui_parameters['method'] = GuiParam(parent_widget = self.box, label = 'Method:', list_values = method_names, callback_func = self.refresh_method)

        self.method = self.transformers[self.gui_parameters['method'].get_value()]
        obj_name, obj_doc, parameters, full_description = get_object_info(self.method, self.sc)

        # Create method label doc.
        self.method_info_label = QtGui.QLabel(full_description, self.box)
        self.box.layout().addWidget(self.method_info_label)

        self.action_box = gui.widgetBox(self.box)
        # Action Button
        self.create_sc_btn = gui.button(self.action_box, self, label = 'Apply', callback = self.transform)

        self.module = None
        self.method = None
        self.transformers = None
        self.models = None
        self.estimators = None

    def refresh_method(self, text):

        self.method = self.transformers[text]
        obj_name, obj_doc, parameters, full_description = get_object_info(self.method, self.sc)
        self.method_info_label.setText(full_description)

    def get_input(self, obj):
        self.in_df = obj
        self.sc = obj.rdd.ctx
        self.hc = obj.sql_ctx

    def onDeleteWidget(self):
        if self.sc:
            self.sc.stop()

    def transform(self):
        self.conf = SparkConf()
        for key, parameter in self.gui_parameters.items():
            self.conf.set(key, parameter.get_value())

        self.sc = SparkContext(conf = self.conf)
        self.hc = HiveContext(self.sc)
        self.send("SparkContext", self.sc)
        self.send("HiveContext", self.hc)
