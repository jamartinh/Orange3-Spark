from PyQt4 import QtGui
from collections import OrderedDict


def dict_to_text_widgets(params, parent_widget):
    text_widget = OrderedDict()
    for key, value in params.items():
        place_holder_text, default_value = value
        text_widget[key] = QtGui.QLineEdit(parent_widget)
        text_widget[key].setPlaceholderText(place_holder_text)
        parent_widget.layout().addWidget(text_widget[key])

    return text_widget
