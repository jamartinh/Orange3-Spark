__author__ = 'jamh'

from collections import OrderedDict

import pyspark
from Orange.widgets import widget, gui
from PyQt4 import QtGui
from pyspark.sql import HiveContext

from ..base.shared_spark_context import SharedSparkContext
from ..utils.gui_utils import GuiParam
from ..utils.ml_api_utils import get_transformers, get_object_info


class OWSparkTransformer(SharedSparkContext):
    # widget_id = None

    name = "Transformer"
    description = "A Transformer of the Spark ml api"
    icon = "icons/spark.png"
    inputs = [("DataFrame", pyspark.sql.DataFrame, "get_input", widget.Default)]
    outputs = [("DataFrame", pyspark.sql.DataFrame, widget.Dynamic)]

    want_main_area = False
    resizing_enabled = True

    conf = None
    in_df = None
    out_df = None
    obj_type = None
    box_text = "Spark Application"
    module = None
    module_name = None
    method_names = None
    method = None
    method_parameters = None
    box_text = None
    get_modules = get_transformers

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

        self.module_methods = self.get_modules(self.module)
        self.method_names = sorted(self.module_methods.keys())
        self.gui_parameters['method'] = GuiParam(parent_widget = self.box, list_values = self.method_names, callback_func = self.refresh_method)

        # Create method label doc.
        self.method_info_label = QtGui.QTextEdit('', self.help_box)
        self.method_info_label.setAcceptRichText(True)
        self.method_info_label.setReadOnly(True)
        self.method_info_label.autoFormatting()
        self.help_box.layout().addWidget(self.method_info_label)

        # Create place to show/set parameters of method
        self.parameters_box = gui.widgetBox(self.box, 'Parameters:', addSpace = True)

        self.refresh_method(self.gui_parameters['method'].get_value())

        self.action_box = gui.widgetBox(self.box)
        # Action Button
        self.create_sc_btn = gui.button(self.action_box, self, label = 'Apply', callback = self.apply)

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
            list_values = None
            if k.endswith('Col') and (default_value == 'None' or default_value is None) and self.in_df:
                list_values = list(self.in_df.columns)
                default_value = list_values[0]

            self.gui_parameters[k] = GuiParam(parent_widget = self.parameters_box, list_values = list_values, label = k, default_value = str(default_value),
                                              place_holder_text = parameter_doc,
                                              doc_text = parameter_doc)

    def get_input(self, obj):
        self.in_df = obj
        self.refresh_method(self.gui_parameters['method'].get_value())

    def build_param_map(self, method_instance):
        paramMap = dict()
        for k in self.method_parameters:
            value = self.gui_parameters[k].get_usable_value()
            # name = self.gui_parameters[k].get_param_name(self.method.__name__, k)
            paramMap[pyspark.ml.param.Param(method_instance, k, '')] = value
        return paramMap

    def apply(self):
        method_instance = self.method()
        paramMap = self.build_param_map(method_instance)

        self.out_df = method_instance.transform(self.in_df, params = paramMap)
        self.send("DataFrame", self.out_df)
