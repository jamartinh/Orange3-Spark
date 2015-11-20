from PyQt4 import QtGui
from Orange.widgets import widget, gui, settings

class GuiParam:
    widget = None

    def __init__(self,master, parent_widget,, label = None, default_value = None, place_holder_text = None, list_values = None, callback_func = None, doc_text = None, **kwargs):
        """

        :param label: a text label for the GUI control
        :param default_value: a default value to asing to the value of the control in case of empty.
        :param place_holder_text: a text to show when the value of the control is empty, it can be used to avoid use of label.
        :param list_values: a closed list of the values that accepts this parameter, this should create a combobox like control.
        :param callback_func: a call back function when the value of the GUI control changes, e.g. combobox selection.
        :param doc_text: if want to add extra documentation for the parameter, it can be used for a tool tip for instance.
        :param kwargs: used to add extra parameters for future improvements and compatibility.
        :return: an instance of gui_param
        """

        self.default_value = default_value
        self.callback_func = callback_func
        self.parent_widget = parent_widget
        self.hbox = self.parent_widget

        if doc_text:
            self.doc_text = doc_text

        if list_values:
            self.list_values = list_values
            self.gui_type = 'multiple'
            self.widget = create_auto_combobox(parent_widget, self.list_values, callback_func)
        else:
            self.gui_type = 'single'
            self.widget = gui.lineEdit(widget, master, value, label=None, labelWidth=None,
             orientation='vertical', box=None, callback=None,
             valueType=str, validator=None, controlWidth=None,
             callbackOnType=False, focusInCallback=None,
             enterPlaceholder=False, **misc):
            self.widget = QtGui.QLineEdit(parent_widget)
            self.widget.setPlaceholderText(str(place_holder_text))
            if self.default_value:
                self.widget.setText(str(self.default_value))

        if label:
            self.label = label
            self.widget_label = QtGui.QLabel(self.label, self.parent_widget)
            self.widget_label.setBuddy(self.widget)
            self.parent_widget.layout().addWidget(self.widget_label)

        self.parent_widget.layout().addWidget(self.widget)

    def get_value(self):
        if self.gui_type == 'multiple':
            return self.widget.currentText()
        elif self.gui_type == 'single':
            return self.widget.text()
        else:
            return None

    def update(self, values):
        self.widget.clear()
        if self.gui_type == 'multiple':
            for val in values:
                self.widget.addItem(val)
        else:
            self.widget.setText(values)


def create_auto_combobox(parent_widget, values, callback_func = None):
    combo = QtGui.QComboBox(parent_widget)
    for val in values:
        combo.addItem(val)

    combo.activated[str].connect(callback_func)
    return combo
