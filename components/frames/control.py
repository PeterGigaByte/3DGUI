from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton, QProgressBar


class ControlFrame(QFrame):
    def __init__(self, vtk_api, bottom_dock_widget, parent=None):
        super(ControlFrame, self).__init__(parent)
        self.vtk_api = vtk_api
        self.bottom_dock_widget = bottom_dock_widget

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        # Buttons
        # Play button
        self.play_button = QPushButton("Play")
        layout.addWidget(self.play_button)
        self.play_button.clicked.connect(self.on_play_button_clicked)

        # Pause button
        self.pause_button = QPushButton("Pause")
        layout.addWidget(self.pause_button)

        # Reset button
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

    def on_play_button_clicked(self):
        # Replace source_position and destination_position with the positions of your source and destination nodes
        # ON PLAY BUTTON NEEDS TO BE CALLED FUNCTION THAT WILL START ANIMATION
        # IT NEEDS DATA INPUT
        source_position = [0, 0, 10]
        destination_position = [50, -50, 10]

        self.vtk_api.animate_packet_transfer(source_position, destination_position)
        self.bottom_dock_widget.log("Play button pressed - Animation started.")
