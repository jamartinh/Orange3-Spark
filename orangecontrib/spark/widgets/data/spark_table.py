__author__ = 'jamh'
from collections import OrderedDict

import pyspark
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from pyspark.sql import HiveContext

from orangecontrib.spark.base.shared_spark_context import SharedSparkContext
from orangecontrib.spark.utils.gui_utils import GuiParam


class OWSparkSQLTableContext(SharedSparkContext, widget.OWWidget):
    priority = 1
    name = "Hive Table"
    description = "Create a Spark DataFrame from a Hive Table"
    icon = "../icons/Hive.png"
    outputs = [("DataFrame", pyspark.sql.DataFrame, widget.Dynamic)]

    want_main_area = False
    resizing_enabled = True
    databases = ['default']
    tables = list()
    out_df = None
    database = ''
    table = ''
    saved_gui_params = Setting(OrderedDict())

    def __init__(self):
        super().__init__()

        # The main label of the Control's GUI.
        # gui.label(self.controlArea, self, "Spark Context")

        # Create parameters Box.
        box = gui.widgetBox(self.controlArea, "Spark SQL Table", addSpace = True)

        self.gui_parameters = OrderedDict()

        if self.hc:
            self.databases = [i.result for i in self.hc.sql("show databases").collect()]

        default_value = self.saved_gui_params.get('database', 'default')
        if default_value not in self.databases:
            self.databases.append(default_value)
        self.refresh_databases_btn = gui.button(box, self, label = 'Refresh databases', callback = self.fill_database_list)
        self.gui_parameters['database'] = GuiParam(parent_widget = box, list_values = self.databases, label = 'Database', default_value = default_value,
                                                   callback_func = self.refresh_database)

        default_value = self.saved_gui_params.get('table', '')
        self.gui_parameters['table'] = GuiParam(parent_widget = box, label = 'Table', default_value = default_value, list_values = [default_value])
        self.refresh_database(self.gui_parameters['database'].get_value())

        action_box = gui.widgetBox(box)
        # Action Button
        self.create_sc_btn = gui.button(action_box, self, label = 'Submit', callback = self.submit)

    def fill_database_list(self):
        if self.hc:
            self.databases = [i.result for i in self.hc.sql("show databases").collect()]
            self.gui_parameters['database'].update(values = self.databases)

    def refresh_database(self, text):
        if self.hc is None:
            return
        self.database = text
        if self.databases and self.databases != '':
            self.tables = self.hc.tableNames(self.database)
            self.gui_parameters['table'].update(values = self.tables)

    def dummy_func(self):
        pass

    def submit(self):
        if self.hc is None:
            return
        self.table = self.gui_parameters['table'].get_value()
        self.out_df = self.hc.table(self.database + '.' + self.table)
        self.send("DataFrame", self.out_df)
        self.update_saved_gui_parameters()
        self.hide()

    def update_saved_gui_parameters(self):
        for k in self.gui_parameters:
            self.saved_gui_params[k] = self.gui_parameters[k].get_value()
