from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QMenu, QFrame, QVBoxLayout, QFileDialog, QStackedWidget, QLabel
)

from api.animation import AnimationApi
from api.parser import ParserAPI
from api.rendering import EnvironmentRenderingApi
from components.dock_widgets.bottom_dock_widget import BottomDockWidget
from components.dock_widgets.left_dock_widget import LeftDockWidget
from components.dock_widgets.right_dock_widget import RightDockWidget
from components.frames.bottom import BottomFrame
from components.frames.control import ControlFrame
from components.tutorialPopUp import show_tutorial
from interactors.interactors import CustomInteractorStyle, KeyPressInteractor
from network_elements.elements import Node

from parsers.xml.tree_element import ElementTreeXMLParser
from step.step_processor import StepProcessor
from utils.manage import get_objects_by_type
from views.manage.manage import ManageCustomView
from views.settings import SettingsView


class Environment(QMainWindow):
    def __init__(self, parent=None):
        super(Environment, self).__init__(parent)

        # Initialize class attributes
        self.bottom_dock_widget = None
        self.interactor = None
        self.visualizing_frame = None
        self.left_dock_widget = LeftDockWidget(self)
        self.right_dock_widget = RightDockWidget(self)
        self.bottom_dock_widget = BottomDockWidget(self)
        self.setWindowTitle("Environment Visualization")
        self.resize(1000, 800)

        # Initialize ParserAPI and register parsers
        self.parser_api = ParserAPI()
        self.parser_api.register_parser('xml', ElementTreeXMLParser(bottom_dock_widget=self.bottom_dock_widget))
        # self.parser_api.register_parser('xml', DOMXMLParser())
        # self.parser_api.register_parser('json', JSONParser())

        # Initialize EnvironmentRenderingApi
        self.vtk_api = EnvironmentRenderingApi()
        self.renderer = self.vtk_api.get_renderer()

        # Initialize StepProcessor
        self.step_processor = StepProcessor()

        # Initialize AnimationAPI
        self.animation_api = AnimationApi(self.vtk_api)

        self.interactor_style = CustomInteractorStyle()

        # Initialize StackedWidget
        self.stacked_widget = QStackedWidget()

        # Create menu and render window
        self.create_menu()

        # initialize StepProcessor
        self.step_processor = StepProcessor()

        # Initialize views
        self.visualizing_view_widget = self.create_visualizing_view()
        self.settings_view_widget = SettingsView()
        self.manage_custom_view_widget = ManageCustomView(self)

        # Add views to the stacked widget
        self.stacked_widget.addWidget(self.visualizing_view_widget)
        self.stacked_widget.addWidget(self.settings_view_widget)
        self.stacked_widget.addWidget(self.manage_custom_view_widget)

        # Set the initial view
        self.stacked_widget.setCurrentWidget(self.visualizing_view_widget)

        # Set the central widget to the stacked widget
        self.setCentralWidget(self.stacked_widget)

    def create_menu(self):
        """Create the menu bar for the application."""

        # Open file menu
        open_file = QMenu("File", self)
        open_file.addAction("Open File", self.open_file)

        # View menu
        view_menu = QMenu("View", self)
        view_menu.addAction("Visualizing", self.visualizing_view)
        view_menu.addAction("Settings", self.settings_view)
        view_menu.addAction("Manage custom", self.manage_custom_view)

        # Help menu
        help_menu = QMenu("Help", self)
        help_menu.addAction("Tutorial", show_tutorial)

        # Menu bar
        menu_bar = self.menuBar()
        menu_bar.addMenu(open_file)
        menu_bar.addMenu(view_menu)
        menu_bar.addMenu(help_menu)

    def visualizing_view(self):
        """Switch to the visualizing view."""
        self.stacked_widget.setCurrentWidget(self.visualizing_view_widget)

    def settings_view(self):
        """Switch to the settings view."""
        self.stacked_widget.setCurrentWidget(self.settings_view_widget)

    def manage_custom_view(self):
        """Switch to the manage custom objects view."""
        self.stacked_widget.setCurrentWidget(self.manage_custom_view_widget)

    def create_visualizing_view(self):
        """Create the visualizing view."""
        visualizing_view = QFrame(self)
        self.setCentralWidget(visualizing_view)

        # interactor
        self.interactor = KeyPressInteractor(visualizing_view)
        self.interactor.Initialize()

        self.interactor.setFocusPolicy(Qt.StrongFocus)
        self.interactor.setFocus()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Visualisation view"))

        # Top control frame init
        control_frame = ControlFrame(vtk_api=self.vtk_api, animation_api=self.animation_api, bottom_dock_widget=self.bottom_dock_widget)
        self.animation_api.set_control_update_callback(control_frame.update_status)
        self.animation_api.set_max_steps_callback(control_frame.update_max_step_slider)

        # Left dock Widget frame init
        self.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock_widget)

        # Right dock Widget frame init
        self.addDockWidget(Qt.RightDockWidgetArea, self.right_dock_widget)

        # Bottom dock Widget frame init
        self.addDockWidget(Qt.BottomDockWidgetArea, self.bottom_dock_widget)

        # Bottom Time frame init
        bottom_frame = BottomFrame(self)

        # Adding widgets
        layout.addWidget(control_frame)
        layout.addWidget(self.interactor)
        layout.addWidget(bottom_frame)

        visualizing_view.setLayout(layout)

        render_window = self.interactor.GetRenderWindow()
        render_window.AddRenderer(self.renderer)
        render_window.SetSize(1000, 800)
        render_window.SetWindowName("Environment Visualization")

        self.vtk_api.test_view()  # Test view // remove

        self.interactor_style.SetCurrentRenderer(self.renderer)
        self.interactor.SetInteractorStyle(self.interactor_style)
        return visualizing_view

    def showEvent(self, event):
        """Handle show events for the QMainWindow."""
        super().showEvent(event)
        self.interactor.setFocus()

    def open_file(self):
        """Open a file and process its contents."""
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Xml Files (*.xml);;Json "
                                                                          "Files (*.json)",
                                                   options=options)
        if file_path:
            # Add the code to read the file and process its contents.
            # For example, if the file contains data about nodes and buildings, you can parse the file
            # and create the corresponding nodes and buildings in your visualization.
            # 1. parse_file
            self.bottom_dock_widget.log(f"File opened: {file_path}")
            self.animation_api.set_data(self.parser_api.parse_file(file_path))
            # 2. Update info from parsed data
            self.left_dock_widget.clear_widgets()
            self.left_dock_widget.update_list_widget(self.animation_api.data.content)
            # 3 prepare environment
            self.animation_api.prepare_animation()
            # 4 process data and set to animation
            self.animation_api.set_substeps(self.step_processor.process_steps(self.animation_api.data))
            # 5. remove everything on vtk window create nodes and building
            # 6. save logic
            self.visualizing_view()
