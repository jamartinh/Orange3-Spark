import os.path
import pyodbc

from Orange.widgets.widget import OWWidget
import pandas as pd
import pandas.io.sql as psql

from orangecontrib.spark.utils.data_utils import pandas_to_orange, format_sql
import Orange

# from Orange.widgets import widget, gui, settings
# from Orange.widgets.utils import itemmodels, colorpalette
# from Orange.widgets.visualize.owscatterplotgraph import LegendItem, legend_anchor_pos
# from Orange.widgets.io import FileFormats

from PyQt4.QtGui import (
    QListView, QSizePolicy, QApplication, QAction, QKeySequence,
    QGraphicsLineItem, QSlider, QPainterPath, QSplitter, QPlainTextEdit, QFileDialog
)

from PyQt4 import QtCore
from Orange.widgets import widget, gui, settings


def convert_dataframe_to_orange(df):
    return pandas_to_orange(df)


class OWodbcTable(OWWidget):
    priority = 3
    allSQLSelectWidgets = []
    settingsList = ["recentConnections", "lastQuery"]
    name = "ODBC"
    description = "Create a Table from an ODBC datasource"
    icon = "../icons/sql.png"
    inputs = []
    outputs = [("Data", Orange.data.Table, widget.Default),
               ("Feature Definitions", Orange.data.Domain, widget.Default),
               ("Pandas", pd.DataFrame, widget.Default)]

    settingsHandler = settings.DomainContextHandler()

    def __init__(self):
        super().__init__()
        gui.label(self.controlArea, self, "from pandas:")
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.allSQLSelectWidgets.append(self)  # set default settings
        self.domain = None
        self.recentConnections = list()
        self.recentConnections.append("(none)")

        self.queryFile = None
        self.query = ''
        self.lastQuery = None
        if self.lastQuery is not None:
            self.query = self.lastQuery

        sources = pyodbc.dataSources()
        dsns = list(sources.keys())
        dsns.sort()

        for dsn in dsns:
            self.recentConnections.append("DSN={dsn}".format(dsn = dsn))

        self.connectString = self.recentConnections[0]

        self.connectBox = gui.widgetBox(self.controlArea, "Database")

        self.connectLineEdit = gui.lineEdit(self.connectBox, self, 'connectString', callback = None)
        self.connectCombo = gui.comboBox(self.connectBox, self, 'connectString', items = self.recentConnections, valueType = str, sendSelectedValue = True)
        self.button = gui.button(self.connectBox, self, 'connect', callback = self.connectDB, disabled = 0)
        # query
        self.splitCanvas = QSplitter(QtCore.Qt.Vertical, self.mainArea)
        self.mainArea.layout().addWidget(self.splitCanvas)

        self.textBox = gui.widgetBox(self, 'HiveQL')
        self.splitCanvas.addWidget(self.textBox)
        self.queryTextEdit = QPlainTextEdit(self.query, self)
        self.textBox.layout().addWidget(self.queryTextEdit)

        self.selectBox = gui.widgetBox(self.controlArea, "Select statement")
        # self.selectSubmitBox = QHGroupBox("", self.selectBox)
        # self.queryTextEdit.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        # self.queryTextEdit.setMinimumWidth(300)
        # self.connect(self.queryTextEdit, SIGNAL('returnPressed()'), self.executeQuery)
        gui.button(self.selectBox, self, "Open...", callback = self.openScript)
        gui.button(self.selectBox, self, "Save...", callback = self.saveScript)
        self.selectBox.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        gui.button(self.selectBox, self, 'format SQL!', callback = self.format_sql, disabled = 0)
        gui.button(self.selectBox, self, 'execute!', callback = self.executeQuery, disabled = 0)
        self.domainBox = gui.widgetBox(self.controlArea, "Domain")
        self.domainLabel = gui.label(self.domainBox, self, '')
        # info
        self.infoBox = gui.widgetBox(self.controlArea, "Info")
        self.info = []
        self.info.append(gui.label(self.infoBox, self, 'No data loaded.'))
        self.info.append(gui.label(self.infoBox, self, ''))
        self.resize(300, 300)

        self.cnxn = None

    def destroy(self, destroyWindow, destroySubWindows):
        self.allSQLSelectWidgets.remove(self)
        self.destroy(self, destroyWindow, destroySubWindows)

    def activateLoadedSettings(self):
        # print "activating", self.recentQueries, ", ",self.recentConnections
        self.query = self.lastQuery
        self.setConnectionList()

    def selectConnection(self, n):
        if n < len(self.recentConnections):
            name = self.recentConnections[n]
            self.recentConnections.remove(name)
            self.recentConnections.insert(0, name)
        if len(self.recentConnections) > 0:
            self.setConnectionList()
            self.connectDB(self.recentConnections[0])

    def setInfo(self, info):
        for (i, s) in enumerate(info):
            self.info[i].setText(s)

    def setMeta(self):
        domain = self.data.domain
        # s = "Attrs:\n    " + "\n    ".join([str(i) for i in domain.attributes]) + "\n" + "Class:" + str(domain.classVar)
        # self.domainLabel.setText(s)
        # for i in domain.getmetas():
        # self.propertyCheckBoxes[i].set()

    # checks whether any file widget knows of any variable from the current domain
    def attributesOverlap(self, domain):
        for fw in self.allFileWidgets:
            if fw != self and getattr(fw, "dataDomain", None):
                for var in domain:
                    if var in fw.dataDomain:
                        return True
        return False

    # Execute a query, create data from it and send it over the data channel
    def executeQuery(self, query = None, throughReload = 0, DK = None, DC = None):

        self.connectDB()
        query = self.queryTextEdit.toPlainText()

        if query is None:
            query = str(self.queryTextEdit.toPlainText())
        # try:
        self.pandas = psql.read_sql_query(query, self.cnxn)
        # except Exception:
        #    self.setInfo(('Query failed:', str('')))
        #    df = pd.DataFrame()

        self.data = convert_dataframe_to_orange(self.pandas)

        self.send("Data", self.data)
        self.send("Pandas", self.pandas)
        self.setInfo(('Query returned', 'Read ' + str(len(self.data)) + ' examples!'))
        self.send("Feature Definitions", self.data.domain)
        self.setMeta()
        self.lastQuery = query

    def format_sql(self):
        query = str(self.queryTextEdit.toPlainText())
        str_sql = str(format_sql(query))
        self.queryTextEdit.clear()
        self.queryTextEdit.insertPlainText(str_sql)

    def connectDB(self):
        if self.connectString is None:
            self.connectString = str(self.connectString)
        if self.connectString in self.recentConnections: self.recentConnections.remove(self.connectString)
        self.recentConnections.insert(0, self.connectString)
        print(self.connectString)
        self.cnxn = pyodbc.connect(self.connectString, autocommit = True)

    # set the query combo box
    def setConnectionList(self):
        self.connectCombo.clear()
        if not self.recentConnections:
            self.connectCombo.insertItem("(none)")
        else:
            self.connectLineEdit.setText(self.recentConnections[0])
        for connection in self.recentConnections:
            self.connectCombo.insertItem(connection)
        self.connectCombo.updateGeometry()

    def openScript(self, filename = None):
        if self.queryFile is None:
            self.queryFile = ''
        if filename == None:
            self.queryFile = QFileDialog.getOpenFileName(self, 'Open SQL file', self.queryFile, 'SQL files (*.sql)\nAll files(*.*)')
        else:
            self.queryFile = filename

        if self.queryFile == "": return

        f = open(self.queryFile, 'r')
        self.queryTextEdit.setPlainText(f.read())
        f.close()

    def saveScript(self):
        if self.queryFile is None:
            self.queryFile = ''
        self.queryFile = QFileDialog.getSaveFileName(self, 'Save SQL file', self.queryFile, 'SQL files (*.sql)\nAll files(*.*)')

        if self.queryFile:
            fn = ""
            head, tail = os.path.splitext(self.queryFile)
            if not tail:
                fn = head + ".sql"
            else:
                fn = self.queryFile
            f = open(fn, 'w')
            f.write(self.queryTextEdit.toPlainText())
            f.close()
