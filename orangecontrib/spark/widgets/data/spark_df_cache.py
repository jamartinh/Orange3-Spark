__author__ = 'jamh'

import pyspark
from Orange.widgets import widget
from pyspark.sql import HiveContext

from orangecontrib.spark.base.shared_spark_context import SharedSparkContext


class OWSparkMLMOdel(SharedSparkContext, widget.OWWidget):
    priority = 6
    name = "Cache DataFrame"
    description = "Call DataFrame.cache(), executes all pending steps on the tasks graph"
    icon = "../icons/Preprocess.svg"
    inputs = [("DataFrame", pyspark.sql.DataFrame, "get_input_df", widget.Default)]
    outputs = [("DataFrame", pyspark.sql.DataFrame, widget.Dynamic)]

    want_main_area = False
    resizing_enabled = True

    conf = None
    in_df = None
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
        self.out_df = self.in_df.cache()
        self.send("DataFrame", self.out_df)
