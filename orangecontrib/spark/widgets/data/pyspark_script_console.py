import keyword
import os
import sys
import unicodedata

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils import itemmodels
from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QRegExp, QByteArray
from PyQt4.QtGui import (
    QFont, QColor, QPalette, QListView, QSizePolicy, QAction,
    QMenu, QKeySequence, QSplitter, QToolButton, QItemSelectionModel,
    QFileDialog
)
from qtconsole.inprocess import QtInProcessKernelManager
from qtconsole.rich_jupyter_widget import RichIPythonWidget


class EmbedIPython(RichIPythonWidget):
    def __init__(self, **kwarg):
        super(RichIPythonWidget, self).__init__()
        self.kernel_manager = QtInProcessKernelManager()
        self.kernel_manager.start_kernel()
        self.kernel = self.kernel_manager.kernel
        self.kernel.gui = 'qt4'
        self.kernel.shell.push(kwarg)
        self.kernel_client = self.kernel_manager.client()
        self.kernel_client.start_channels()


def text_format(foreground = Qt.black, weight = QFont.Normal):
    fmt = QtGui.QTextCharFormat()
    fmt.setForeground(QtGui.QBrush(foreground))
    fmt.setFontWeight(weight)
    return fmt


class PythonSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent = None):

        self.keywordFormat = text_format(Qt.blue, QFont.Bold)
        self.stringFormat = text_format(Qt.darkGreen)
        self.defFormat = text_format(Qt.black, QFont.Bold)
        self.commentFormat = text_format(Qt.lightGray)
        self.decoratorFormat = text_format(Qt.darkGray)

        self.keywords = list(keyword.kwlist)

        self.rules = [(QRegExp(r"\b%s\b" % kwd), self.keywordFormat)
                      for kwd in self.keywords] + \
                     [(QRegExp(r"\bdef\s+([A-Za-z_]+[A-Za-z0-9_]+)\s*\("),
                       self.defFormat),
                      (QRegExp(r"\bclass\s+([A-Za-z_]+[A-Za-z0-9_]+)\s*\("),
                       self.defFormat),
                      (QRegExp(r"'.*'"), self.stringFormat),
                      (QRegExp(r'".*"'), self.stringFormat),
                      (QRegExp(r"#.*"), self.commentFormat),
                      (QRegExp(r"@[A-Za-z_]+[A-Za-z0-9_]+"),
                       self.decoratorFormat)]

        self.multilineStart = QRegExp(r"(''')|" + r'(""")')
        self.multilineEnd = QRegExp(r"(''')|" + r'(""")')

        super().__init__(parent)

    def highlightBlock(self, text):
        for pattern, format in self.rules:
            exp = QRegExp(pattern)
            index = exp.indexIn(text)
            while index >= 0:
                length = exp.matchedLength()
                if exp.numCaptures() > 0:
                    self.setFormat(exp.pos(1), len(str(exp.cap(1))), format)
                else:
                    self.setFormat(exp.pos(0), len(str(exp.cap(0))), format)
                index = exp.indexIn(text, index + length)

        # Multi line strings
        start = self.multilineStart
        end = self.multilineEnd

        self.setCurrentBlockState(0)
        startIndex, skip = 0, 0
        if self.previousBlockState() != 1:
            startIndex, skip = start.indexIn(text), 3
        while startIndex >= 0:
            endIndex = end.indexIn(text, startIndex + skip)
            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLen = len(text) - startIndex
            else:
                commentLen = endIndex - startIndex + 3
            self.setFormat(startIndex, commentLen, self.stringFormat)
            startIndex, skip = (start.indexIn(text,
                                              startIndex + commentLen + 3),
                                3)


class PythonScriptEditor(QtGui.QPlainTextEdit):
    INDENT = 4

    def lastLine(self):
        text = str(self.toPlainText())
        pos = self.textCursor().position()
        index = text.rfind("\n", 0, pos)
        text = text[index: pos].lstrip("\n")
        return text

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            text = self.lastLine()
            indent = len(text) - len(text.lstrip())
            if text.strip() == "pass" or text.strip().startswith("return "):
                indent = max(0, indent - self.INDENT)
            elif text.strip().endswith(":"):
                indent += self.INDENT
            super().keyPressEvent(event)
            self.insertPlainText(" " * indent)
        elif event.key() == Qt.Key_Tab:
            self.insertPlainText(" " * self.INDENT)
        elif event.key() == Qt.Key_Backspace:
            text = self.lastLine()
            if text and not text.strip():
                cursor = self.textCursor()
                for i in range(min(self.INDENT, len(text))):
                    cursor.deletePreviousChar()
            else:
                super().keyPressEvent(event)

        else:
            super().keyPressEvent(event)


def interleave(seq1, seq2):
    """
    Interleave elements of `seq2` between consecutive elements of `seq1`.

        >>> list(interleave([1, 3, 5], [2, 4]))
        [1, 2, 3, 4, 5]

    """
    iterator1, iterator2 = iter(seq1), iter(seq2)
    leading = next(iterator1)
    for element in iterator1:
        yield leading
        yield next(iterator2)
        leading = element

    yield leading


class Script(object):
    Modified = 1
    MissingFromFilesystem = 2

    def __init__(self, name, script, flags = 0, filename = None):
        self.name = name
        self.script = script
        self.flags = flags
        self.filename = filename


class ScriptItemDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)

    def displayText(self, script, locale):
        if script.flags & Script.Modified:
            return "*" + script.name
        else:
            return script.name

    def paint(self, painter, option, index):
        script = index.data(Qt.DisplayRole)

        if script.flags & Script.Modified:
            option = QtGui.QStyleOptionViewItemV4(option)
            option.palette.setColor(QPalette.Text, QColor(Qt.red))
            option.palette.setColor(QPalette.Highlight, QColor(Qt.darkRed))
        super().paint(painter, option, index)

    def createEditor(self, parent, option, index):
        return QtGui.QLineEdit(parent)

    def setEditorData(self, editor, index):
        script = index.data(Qt.DisplayRole)
        editor.setText(script.name)

    def setModelData(self, editor, model, index):
        model[index.row()].name = str(editor.text())


def select_row(view, row):
    """
    Select a `row` in an item view
    """
    selmodel = view.selectionModel()
    selmodel.select(view.model().index(row, 0),
                    QItemSelectionModel.ClearAndSelect)


from orangecontrib.spark.base.shared_spark_context import SharedSparkContext


class OWPySparkScript(SharedSparkContext, widget.OWWidget):
    priority = 3
    name = "PySpark Script"
    description = "Write a PySpark script and run it on input"
    icon = "../icons/PythonScript.svg"

    inputs = [("in_object", object, "setObject")]
    outputs = [("out_object", object, widget.Dynamic)]

    libraryListSource = \
        Setting([Script("Hello world", "print('Hello world')\n")])
    currentScriptIndex = Setting(0)
    splitterState = Setting(None)
    auto_execute = Setting(False)
    _script = Setting("")

    def __init__(self):
        super().__init__()

        self.spark_logo = """
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version {version}
      /_/

""".format(version = self.sc.version)

        self.in_object = None
        self.out_object = None
        self.auto_execute = False

        for s in self.libraryListSource:
            s.flags = 0

        self._cachedDocuments = { }

        self.infoBox = gui.widgetBox(self.controlArea, 'Info')
        gui.label(
                self.infoBox, self,
                "<p>Execute python script.</p><p>Input variables:<ul><li> " + \
                "<li>".join(t.name for t in self.inputs) + \
                "</ul></p><p>Output variables:<ul><li>" + \
                "<li>".join(t.name for t in self.outputs) + \
                "</ul></p>"
        )

        self.libraryList = itemmodels.PyListModel(
                [], self,
                flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)

        self.libraryList.wrap(self.libraryListSource)

        self.controlBox = gui.widgetBox(self.controlArea, 'Library')
        self.controlBox.layout().setSpacing(1)

        self.libraryView = QListView(editTriggers = QListView.DoubleClicked | QListView.EditKeyPressed, sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred))
        self.libraryView.setItemDelegate(ScriptItemDelegate(self))
        self.libraryView.setModel(self.libraryList)

        self.libraryView.selectionModel().selectionChanged.connect(
                self.onSelectedScriptChanged
        )
        self.controlBox.layout().addWidget(self.libraryView)

        w = itemmodels.ModelActionsWidget()

        self.addNewScriptAction = action = QAction("+", self)
        action.setToolTip("Add a new script to the library")
        action.triggered.connect(self.onAddScript)
        w.addAction(action)

        action = QAction(unicodedata.lookup("MINUS SIGN"), self)
        action.setToolTip("Remove script from library")
        action.triggered.connect(self.onRemoveScript)
        w.addAction(action)

        action = QAction("Update", self)
        action.setToolTip("Save changes in the editor to library")
        action.setShortcut(QKeySequence(QKeySequence.Save))
        action.triggered.connect(self.commitChangesToLibrary)
        w.addAction(action)

        action = QAction("More", self, toolTip = "More actions")

        new_from_file = QAction("Import a script from a file", self)
        save_to_file = QAction("Save selected script to a file", self)
        save_to_file.setShortcut(QKeySequence(QKeySequence.SaveAs))

        new_from_file.triggered.connect(self.onAddScriptFromFile)
        save_to_file.triggered.connect(self.saveScript)

        menu = QMenu(w)
        menu.addAction(new_from_file)
        menu.addAction(save_to_file)
        action.setMenu(menu)
        button = w.addAction(action)
        button.setPopupMode(QToolButton.InstantPopup)

        w.layout().setSpacing(1)

        self.controlBox.layout().addWidget(w)

        gui.auto_commit(self.controlArea, self, "auto_execute", "Execute")

        self.splitCanvas = QSplitter(Qt.Vertical, self.mainArea)
        self.mainArea.layout().addWidget(self.splitCanvas)

        self.defaultFont = defaultFont = \
            "Monaco" if sys.platform == "darwin" else "Courier"

        self.textBox = gui.widgetBox(self, 'Python script')
        self.splitCanvas.addWidget(self.textBox)
        self.text = PythonScriptEditor(self)
        self.textBox.layout().addWidget(self.text)

        self.textBox.setAlignment(Qt.AlignVCenter)
        self.text.setTabStopWidth(4)

        self.text.modificationChanged[bool].connect(self.onModificationChanged)

        self.saveAction = action = QAction("&Save", self.text)
        action.setToolTip("Save script to file")
        action.setShortcut(QKeySequence(QKeySequence.Save))
        action.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        action.triggered.connect(self.saveScript)

        self.consoleBox = gui.widgetBox(self, 'Console')
        self.splitCanvas.addWidget(self.consoleBox)

        self.__dict__['sc'] = self._sc
        self.__dict__['hc'] = self._hc

        # self.console = PySparkConsole(self.__dict__, self, sc = self.sc)
        self.console = EmbedIPython(sc = self._sc, hc = self._hc, in_object = self.in_object, out_object = self.out_object)
        self.console.kernel.shell.run_cell('%pylab qt')
        self.console.kernel.shell.run_cell("print('{sparklogo}')".format(sparklogo = self.spark_logo))
        self.consoleBox.layout().addWidget(self.console)
        # self.console.document().setDefaultFont(QFont(defaultFont))
        self.consoleBox.setAlignment(Qt.AlignBottom)
        # self.console.setTabStopWidth(4)

        select_row(self.libraryView, self.currentScriptIndex)

        self.splitCanvas.setSizes([2, 1])
        if self.splitterState is not None:
            self.splitCanvas.restoreState(QByteArray(self.splitterState))

        self.splitCanvas.splitterMoved[int, int].connect(self.onSpliterMoved)
        self.controlArea.layout().addStretch(1)
        self.resize(800, 600)

    def setObject(self, obj):
        self.in_object = obj

    def handleNewSignals(self):
        self.unconditional_commit()

    def selectedScriptIndex(self):
        rows = self.libraryView.selectionModel().selectedRows()
        if rows:
            return [i.row() for i in rows][0]
        else:
            return None

    def setSelectedScript(self, index):
        select_row(self.libraryView, index)

    def onAddScript(self, *args):
        self.libraryList.append(Script("New script", "", 0))
        self.setSelectedScript(len(self.libraryList) - 1)

    def onAddScriptFromFile(self, *args):
        filename = QFileDialog.getOpenFileName(
                self, 'Open Python Script',
                os.path.expanduser("~/"),
                'Python files (*.py)\nAll files(*.*)'
        )

        filename = str(filename)
        if filename:
            name = os.path.basename(filename)
            contents = open(filename, "rb").read().decode("utf-8", errors = "ignore")
            self.libraryList.append(Script(name, contents, 0, filename))
            self.setSelectedScript(len(self.libraryList) - 1)

    def onRemoveScript(self, *args):
        index = self.selectedScriptIndex()
        if index is not None:
            del self.libraryList[index]
            select_row(self.libraryView, max(index - 1, 0))

    def onSaveScriptToFile(self, *args):
        index = self.selectedScriptIndex()
        if index is not None:
            self.saveScript()

    def onSelectedScriptChanged(self, selected, deselected):
        index = [i.row() for i in selected.indexes()]
        if index:
            current = index[0]
            if current >= len(self.libraryList):
                self.addNewScriptAction.trigger()
                return

            self.text.setDocument(self.documentForScript(current))
            self.currentScriptIndex = current

    def documentForScript(self, script = 0):
        if type(script) != Script:
            script = self.libraryList[script]

        if script not in self._cachedDocuments:
            doc = QtGui.QTextDocument(self)
            doc.setDocumentLayout(QtGui.QPlainTextDocumentLayout(doc))
            doc.setPlainText(script.script)
            doc.setDefaultFont(QFont(self.defaultFont))
            doc.highlighter = PythonSyntaxHighlighter(doc)
            doc.modificationChanged[bool].connect(self.onModificationChanged)
            doc.setModified(False)
            self._cachedDocuments[script] = doc
        return self._cachedDocuments[script]

    def commitChangesToLibrary(self, *args):
        index = self.selectedScriptIndex()
        if index is not None:
            self.libraryList[index].script = self.text.toPlainText()
            self.text.document().setModified(False)
            self.libraryList.emitDataChanged(index)

    def onModificationChanged(self, modified):
        index = self.selectedScriptIndex()
        if index is not None:
            self.libraryList[index].flags = Script.Modified if modified else 0
            self.libraryList.emitDataChanged(index)

    def onSpliterMoved(self, pos, ind):
        self.splitterState = str(self.splitCanvas.saveState())

    def updateSelecetdScriptState(self):
        index = self.selectedScriptIndex()
        if index is not None:
            script = self.libraryList[index]
            self.libraryList[index] = Script(script.name,
                                             self.text.toPlainText(),
                                             0)

    def saveScript(self):
        index = self.selectedScriptIndex()
        if index is not None:
            script = self.libraryList[index]
            filename = script.filename
        else:
            filename = os.path.expanduser("~/")

        filename = QFileDialog.getSaveFileName(
                self, 'Save Python Script',
                filename,
                'Python files (*.py)\nAll files(*.*)'
        )

        if filename:
            fn = ""
            head, tail = os.path.splitext(filename)
            if not tail:
                fn = head + ".py"
            else:
                fn = filename

            f = open(fn, 'w')
            f.write(self.text.toPlainText())
            f.close()

    def commit(self):
        self._script = str(self.text.toPlainText())
        self.console.execute(self._script)
