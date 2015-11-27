__author__ = 'jamh'
from collections import OrderedDict

import pyspark
from Orange.widgets import widget, gui
from pyspark.sql import HiveContext

from orangecontrib.spark.base.shared_spark_context import SharedSparkContext
from orangecontrib.spark.utils.gui_utils import GuiParam


class OWSparkSQLTableContext(SharedSparkContext, widget.OWWidget):
    name = "Hive Table"
    description = "Create a Spark DataFrame from a Hive Table"
    icon = "../icons/Hive.png"
    outputs = [("DataFrame", pyspark.sql.DataFrame, widget.Dynamic)]

    want_main_area = False
    resizing_enabled = True
    databases = list()
    tables = list()
    out_df = None
    database = None
    table = None

    def __init__(self):
        super().__init__()

        # The main label of the Control's GUI.
        # gui.label(self.controlArea, self, "Spark Context")

        # Create parameters Box.
        box = gui.widgetBox(self.controlArea, "Spark SQL Table", addSpace = True)

        self.gui_parameters = OrderedDict()

        if self.hc:
            self.databases = [i.result for i in self.hc.sql("show databases").collect()]

        self.gui_parameters['database'] = GuiParam(parent_widget = box, list_values = self.databases, label = 'Database:', default_value = 'default',
                                                   callback_func = self.refresh_database)

        self.gui_parameters['table'] = GuiParam(parent_widget = box, label = 'Table:', list_values = [''])
        self.refresh_database(self.gui_parameters['database'].get_value())

        action_box = gui.widgetBox(box)
        # Action Button
        self.create_sc_btn = gui.button(action_box, self, label = 'Submit', callback = self.submit)

    def refresh_database(self, text):
        self.database = text
        if self.databases and self.databases != '':
            self.tables = self.hc.tableNames(self.database)
            self.gui_parameters['table'].update(values = self.tables)

    def dummy_func(self):
        pass

    def submit(self):
        self.table = self.gui_parameters['table'].get_value()
        self.out_df = self.hc.table(self.database + '.' + self.table)
        self.send("DataFrame", self.out_df)
