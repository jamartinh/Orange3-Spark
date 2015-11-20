import pyspark
from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import OWWidget
from PyQt4 import QtCore
from PyQt4.QtGui import (
    QSizePolicy, QSplitter, QPlainTextEdit
)

from orangecontrib.spark.utils.bdutils import pandas_to_orange, format_sql


def convert_dataframe_to_orange(df):
    return pandas_to_orange(df)


class OWSparkDataFrame(OWWidget):
    allSQLSelectWidgets = []
    settingsList = ["lastQuery"]
    name = "SparkSQL"
    description = "Create a Spark Dataframe from an SparkSQL source"
    icon = "icons/sparksql.png"
    inputs = [("SparkSQLContext", pyspark.sql.HiveContext, "get_input", widget.Default)]
    outputs = [("DataFrame", pyspark.sql.DataFrame, widget.Dynamic),
               ("SparkContext", pyspark.SparkContext, widget.Default),
               ("HiveContext", pyspark.sql.HiveContext, widget.Default)
               ]

    settingsHandler = settings.DomainContextHandler()

    def __init__(self):
        super().__init__()
        gui.label(self.controlArea, self, "Spark DataFrame")
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.allSQLSelectWidgets.append(self)  # set default settings
        self.domain = None

        self.queryFile = None
        self.query = ''
        self.lastQuery = None
        # self.loadSettings()
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

        self.HC = None
        self.obj_type = None
        self.sdf = None
        self.sc = None

    def get_input(self, obj):
        self.obj_type = self.NOTHING if obj is None else type(obj).__name__
        self.HC = obj
        self.sc = obj.rdd.ctx

    def destroy(self, destroyWindow, destroySubWindows):
        self.allSQLSelectWidgets.remove(self)
        self.destroy(self, destroyWindow, destroySubWindows)

    def activateLoadedSettings(self):
        # print "activating", self.recentQueries, ", ",self.recentConnections
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

        query = self.queryTextEdit.toPlainText()

        if query is None:
            return None

        self.sdf = self.HC.sql(query)
        self.send("DataFrame", self.sdf)
        self.send("SparkContext", self.sc)
        self.send("HiveContext", self.HC)
        # self.data = convert_dataframe_to_orange(self.pandas)
        # self.send("Table", self.data)
        # self.setInfo(('Query returned', 'Read ' + str(len(self.data)) + ' examples!'))
        # self.send("Pandas", self.pandas)

        # self.setMeta()
        self.lastQuery = query

    def format_sql(self):
        query = str(self.queryTextEdit.toPlainText())
        str_sql = str(format_sql(query))
        self.queryTextEdit.clear()
        self.queryTextEdit.insertPlainText(str_sql)

        # set the query combo box
