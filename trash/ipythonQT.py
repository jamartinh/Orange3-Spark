__author__ = "Jose Antonio Martin H."

from qtconsole.rich_jupyter_widget import RichIPythonWidget
from qtconsole.inprocess import QtInProcessKernelManager
from PyQt4 import QtGui


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


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.textEdit = QtGui.QTextEdit()

        but1 = QtGui.QPushButton('write')
        but1.clicked.connect(self.but_write)

        but2 = QtGui.QPushButton('read')
        but2.clicked.connect(self.but_read)

        self.a = { 'text': '' }
        self.console = EmbedIPython(testing = 123, a = self.a)
        self.console.kernel.shell.run_cell('%pylab qt')

        vbox = QtGui.QVBoxLayout()
        hbox = QtGui.QHBoxLayout()
        vbox.addWidget(self.textEdit)
        vbox.addWidget(self.console)
        hbox.addWidget(but1)
        hbox.addWidget(but2)
        vbox.addLayout(hbox)

        b = QtGui.QWidget()
        b.setLayout(vbox)
        self.setCentralWidget(b)

    def but_read(self):
        self.a['text'] = self.textEdit.toPlainText()
        self.console.execute("print('a[\\\'text\\\'] = \"'+ a['text'] +'\"')")

    def but_write(self):
        self.textEdit.setText(self.a['text'])


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
