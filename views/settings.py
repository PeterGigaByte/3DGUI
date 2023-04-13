from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel


class SettingsView(QFrame):
    def __init__(self, parent=None):
        super(SettingsView, self).__init__(parent)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings view"))
        self.setLayout(layout)
