__author__ = 'jamh'

from collections import OrderedDict

import pyspark
from Orange.widgets import widget, gui
from PyQt4 import QtGui
from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext

from ..utils.gui_utils import GuiParam
from ..utils.ml_api_utils import get_transformers, get_object_info


class OWSparkTransformer:
    # widget_id = None

    name = "Transformer"
    description = "A Transformer of the Spark ml api"
    icon = "icons/spark.png"
    inputs = [("DataFrame", pyspark.sql.DataFrame, "get_input", widget.Default)]
    outputs = [("DataFrame", pyspark.sql.DataFrame, widget.Dynamic),
               ("SparkContext", pyspark.SparkContext, widget.Default),
               ("HiveContext", pyspark.sql.HiveContext, widget.Default)
               ]
    # settingsHandler = settings.DomainContextHandler()

    want_main_area = False
    resizing_enabled = True

    conf = None
    sc = None
    hc = None
    in_df = None
    out_df = None
    obj_type = None
    box_text = "Spark Application"
    module = None
    module_name = None
    method_names = None
    box_text = None

    def __init__(self):
        super().__init__()
        # gui.label(self.controlArea, self, "pyspark.ml")

        # Create parameters Box.
        self.main_box = gui.widgetBox(self.controlArea, orientation = 'horizontal', addSpace = True)
        self.box = gui.widgetBox(self.main_box, self.box_text, addSpace = True)
        self.help_box = gui.widgetBox(self.main_box, 'Documentation', addSpace = True)

        # Create module label doc.
        # Unfortunately ml does not have this documentation yet.
        # self.module_info = get_module_info(self.module)
        # self.module_info_label = QtGui.QTextEdit(self.module_info, self.box)
        # self.module_info_label.setAcceptRichText(True)
        # self.module_info_label.setReadOnly(True)
        #
        # self.box.layout().addWidget(self.module_info_label)

        self.gui_parameters = OrderedDict()

        # Create place for selecting the method
        self.module_methods = get_transformers(self.module)
        self.method_names = sorted(self.module_methods.keys())
        self.gui_parameters['method'] = GuiParam(parent_widget = self.box, list_values = self.method_names, callback_func = self.refresh_method)

        self.method = self.module_methods[self.gui_parameters['method'].get_value()]
        obj_name, obj_doc, self.method_parameters, full_description = get_object_info(self.method, self.sc)

        # Create method label doc.
        self.method_info_label = QtGui.QTextEdit(full_description, self.help_box)
        self.method_info_label.setAcceptRichText(True)
        self.method_info_label.setReadOnly(True)
        self.method_info_label.autoFormatting()
        self.help_box.layout().addWidget(self.method_info_label)

        # Create place to show/set parameters of method
        self.parameters_box = gui.widgetBox(self.box, 'Parameters:', addSpace = True)
        layout = self.parameters_box.layout()
        while layout.count():
            item = layout.takeAt(0)
            item.widget().deleteLater()

        for k, v in self.method_parameters.items():
            default_value = v[1]
            parameter_doc = v[-1]
            self.gui_parameters[k] = GuiParam(parent_widget = self.parameters_box, label = k, default_value = str(default_value), place_holder_text = parameter_doc,
                                              doc_text = parameter_doc)

        self.action_box = gui.widgetBox(self.box)
        # Action Button
        self.create_sc_btn = gui.button(self.action_box, self, label = 'Apply', callback = self.transform)

    def refresh_method(self, text):

        self.method = self.module_methods[text]
        obj_name, obj_doc, self.method_parameters, full_description = get_object_info(self.method, self.sc)
        self.method_info_label.setText(full_description)

        # clear a layout and delete all widgets
        # aLayout is some QLayout for instance
        layout = self.parameters_box.layout()
        while layout.count():
            item = layout.takeAt(0)
            item.widget().deleteLater()

        for k, v in self.method_parameters.items():
            default_value = v[1]
            parameter_doc = v[-1]
            self.gui_parameters[k] = GuiParam(parent_widget = self.parameters_box, label = k, default_value = str(default_value), place_holder_text = parameter_doc,
                                              doc_text = parameter_doc)

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
