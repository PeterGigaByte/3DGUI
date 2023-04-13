from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget, QListWidget


class LeftDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super(LeftDockWidget, self).__init__("Nodes", parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea)
        list_widget = QListWidget()
        list_widget.addItems(['Node 1', 'Node 2', 'Node 3'])
        self.setWidget(list_widget)
