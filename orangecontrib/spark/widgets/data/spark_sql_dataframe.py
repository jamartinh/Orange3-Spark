import pyspark
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from Orange.widgets.widget import OWWidget
from PyQt4 import QtCore
from PyQt4.QtGui import (
    QSizePolicy, QSplitter, QPlainTextEdit
)

from orangecontrib.spark.base.shared_spark_context import SharedSparkContext
from orangecontrib.spark.utils.data_utils import pandas_to_orange, format_sql


def convert_dataframe_to_orange(df):
    return pandas_to_orange(df)


class OWSparkDataFrame(SharedSparkContext, OWWidget):
    priority = 2
    allSQLSelectWidgets = []
    lastQuery = Setting('')
    name = "Data Frame"
    description = "Create a Spark Dataframe from an SparkSQL source"
    icon = "../icons/sql.png"

    outputs = [("DataFrame", pyspark.sql.DataFrame, widget.Dynamic)]
    out_df = None

    def __init__(self):
        super().__init__()
        gui.label(self.controlArea, self, "Spark DataFrame")
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.allSQLSelectWidgets.append(self)  # set default settings
        self.domain = None

        self.queryFile = None
        self.query = ''
        if self.lastQuery is not None:
            self.query = self.lastQuery

        # query
        self.splitCanvas = QSplitter(QtCore.Qt.Vertical, self.mainArea)
        self.mainArea.layout().addWidget(self.splitCanvas)

        self.textBox = gui.widgetBox(self, 'SparkSQL')
        self.splitCanvas.addWidget(self.textBox)
        self.queryTextEdit = QPlainTextEdit(self.query, self)
        self.textBox.layout().addWidget(self.queryTextEdit)

        self.selectBox = gui.widgetBox(self.controlArea, "Select statement")
        self.selectBox.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        gui.button(self.selectBox, self, 'format SQL!', callback = self.format_sql, disabled = 0)
        gui.button(self.selectBox, self, 'execute!', callback = self.executeQuery, disabled = 0)

        # info
        self.infoBox = gui.widgetBox(self.controlArea, "Info")
        self.info = []
        self.info.append(gui.label(self.infoBox, self, 'No data loaded.'))
        self.info.append(gui.label(self.infoBox, self, ''))
        self.resize(300, 300)

    def destroy(self, destroyWindow, destroySubWindows):
        self.allSQLSelectWidgets.remove(self)
        self.destroy(self, destroyWindow, destroySubWindows)

    def activateLoadedSettings(self):
        self.query = self.lastQuery

    def setInfo(self, info):
        pass
        # for (i, s) in enumerate(info):
        #    self.info[i].setText(s)

    def setMeta(self):
        pass
        # domain = self.data.domain
        # s = "Attrs:\n    " + "\n    ".join([str(i) for i in domain.attributes]) + "\n" + "Class:" + str(domain.classVar)
        # self.domainLabel.setText(s)
        # for i in domain.getmetas():
        # self.propertyCheckBoxes[i].set()

    # Execute a query, create data from it and send it over the data channel
    def executeQuery(self):
        if not self.sc or not self.hc:
            return

        query = self.queryTextEdit.toPlainText()

        if query is None:
            return None

        self.out_df = self.hc.sql(query)
        self.lastQuery = query
        self.send("DataFrame", self.out_df)

    def format_sql(self):
        query = str(self.queryTextEdit.toPlainText())
        str_sql = str(format_sql(query))
        self.queryTextEdit.clear()
        self.queryTextEdit.insertPlainText(str_sql)
