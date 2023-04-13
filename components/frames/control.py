from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton, QProgressBar


class ControlFrame(QFrame):
    def __init__(self, parent=None):
        super(ControlFrame, self).__init__(parent)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        # Buttons
        self.play_button = QPushButton("Play")
        layout.addWidget(self.play_button)
        self.pause_button = QPushButton("Pause")
        layout.addWidget(self.pause_button)
        self.reset_button = QPushButton("Reset")
        layout.addWidget(self.reset_button)

        # Add progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def show_progress_bar(self):
        """Show the progress bar."""
        self.progress_bar.show()  # Show the progress bar

    def update_progress_bar(self, value):
        """Update the value of the progress bar."""
        self.progress_bar.setValue(value)  # Update the value of the progress bar
