from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel


class SettingsView(QFrame):
    """
    A view for application settings.
    """
    def __init__(self, parent=None):
        """
        Initializes the view with a QVBoxLayout and QLabel.
        """
        super(SettingsView, self).__init__(parent)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings view"))
        self.setLayout(layout)
