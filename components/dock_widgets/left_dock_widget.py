from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget, QListWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QWidget

from network_elements.elements import Node, NonP2pLinkProperties
from utils.manage import get_objects_by_type, get_nonp2p_link_properties_by_node_id


class LeftDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super(LeftDockWidget, self).__init__("Nodes", parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea)

        # Create the list widget and add it to the layout
        self.list_widget = QListWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)

        # Create the tree widget and add it to the layout
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        layout.addWidget(self.tree_widget)

        # Initialize empty node dictionary
        self.nodes = {}

        # Connect to the list widget's item selection changed signal and update the tree widget's content accordingly
        self.list_widget.itemSelectionChanged.connect(self.update_tree_widget)

        # Create a widget to hold the layout and set it as the dock widget's widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setWidget(widget)

    def add_node(self, node_id, properties=None):
        if properties is None:
            properties = []

        self.list_widget.addItem(f"Node {node_id}")
        self.nodes[node_id] = {"properties": properties}

    def add_node_property(self, node_id, property_name, values):
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} does not exist")

        root_item = QTreeWidgetItem(None, [property_name])  # Set the parent to None
        for value in values:
            QTreeWidgetItem(root_item, [value])

        self.nodes[node_id]["properties"].append(root_item)

    def update_node_property(self, node_id, property_name, values):
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} does not exist")

        for prop in self.nodes[node_id]["properties"]:
            if prop.text(0) == property_name:
                for i, value in enumerate(values):
                    prop.child(i).setText(0, value)

    def update_tree_widget(self):
        selected_items = self.list_widget.selectedItems()
        if len(selected_items) > 0:
            selected_item = selected_items[0].text()
            node_id = selected_item.split(" ")[1]

            # Clear tree widget and display selected node properties
            self.tree_widget.clear()
            for prop in self.nodes[node_id]["properties"]:
                # Clone the QTreeWidgetItem before adding it to the tree widget
                cloned_prop = prop.clone()
                self.tree_widget.addTopLevelItem(cloned_prop)

    def update_list_widget(self, data):
        node_list = get_objects_by_type(data, Node)
        nonp2p_link_properties_list = get_objects_by_type(data, NonP2pLinkProperties)
        for node in node_list:
            ip_addresses, mac_addresses = get_nonp2p_link_properties_by_node_id(nonp2p_link_properties_list, node.id)
            self.add_node(node.id)
            self.add_node_property(node.id, "IP", ip_addresses)
            self.add_node_property(node.id, "IPV6", [])
            self.add_node_property(node.id, "MAC", mac_addresses)


    
