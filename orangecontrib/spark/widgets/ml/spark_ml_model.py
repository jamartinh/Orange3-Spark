__author__ = 'jamh'

import pyspark
from Orange.widgets import widget
from pyspark.ml import Model
from pyspark.sql import HiveContext

from orangecontrib.spark.base.shared_spark_context import SharedSparkContext


class OWSparkMLMOdel(SharedSparkContext, widget.OWWidget):
    priority = 7
    name = "Model"
    description = "A fitted model"
    icon = "../icons/Normalize.svg"
    inputs = [("DataFrame", pyspark.sql.DataFrame, "get_input_df", widget.Default),
              ("Model", pyspark.ml.Model, "get_input_model", widget.Default)]
    outputs = [("DataFrame", pyspark.sql.DataFrame, widget.Dynamic)]
    # settingsHandler = settings.DomainContextHandler()

    want_main_area = False
    resizing_enabled = True

    conf = None
    in_df = None
    model = None
    out_df = None

    def __init__(self):
        super().__init__()

        # The main label of the Control's GUI.
        # gui.label(self.controlArea, self, "Spark Context")

        # Create parameters Box.
        # box = gui.widgetBox(self.controlArea, "Spark Application", addSpace = True)
        # action_box = gui.widgetBox(box)
        # Action Button
        # self.create_sc_btn = gui.button(action_box, self, label = 'Submit', callback = self.create_context)

    def get_input_df(self, obj):
        self.in_df = obj
        self.transform()

    def get_input_model(self, obj):
        self.model = obj
        self.transform()

    def transform(self):
        if self.in_df and self.model:
            model_instance = self.model()
            #paramMap = self.build_param_map()
            self.out_df = model_instance.transform(self.in_df)
            self.send("DataFrame", self.out_df)
