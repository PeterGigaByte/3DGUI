import uuid
from typing import Dict

import vtk

from api.rendering_objects.building import Building
from api.rendering_objects.ground import Ground
from api.rendering_objects.node import Node
from api.rendering_objects.packet import Packet


def normalize_rgb(rgb):
    return tuple(channel / 255.0 for channel in rgb)


class EnvironmentRenderingApi:
    def __init__(self):
        self.renderer = vtk.vtkRenderer()
        self.setup_renderer()
        self.ground = None
        self.nodes = []
        self.buildings = []
        self.packets = []
        self.packets: Dict[uuid.UUID, Packet] = {}

    def create_ground(self):
        """Create a ground plane for the environment."""
        self.ground = Ground(resolution=(200, 200), origin=(-500, -500, 0), point1=(500, -500, 0),
                             point2=(-500, 500, 0),
                             color=(0, 1, 0))
        self.ground.add_to_renderer(self.renderer)

    def create_building(self, x, y, z, width, height):
        """Create a building at the specified location."""
        building = Building(x=x, y=y, z=z, width=width, height=height)
        building.add_to_renderer(self.renderer)
        self.buildings.append(building)

    def create_node(self, id, x, y, z, radius=1, description="Node", node_color=(255, 0, 0),
                    label_color=(255, 255, 255)):
        """Create a node at the specified location."""
        node = Node(x=float(x), y=float(y), z=float(z), radius=radius, description=description, node_color=node_color,
                    label_color=label_color, node_id=id)
        node.add_to_renderer(renderer=self.renderer)
        self.nodes.append(node)

    def clear_vtk_window(self):
        # Remove all actors from the renderer
        for node in self.nodes:
            sphere_actor, text_actor = node
            self.renderer.RemoveActor(sphere_actor)
            self.renderer.RemoveActor(text_actor)

        # Clear the list of nodes
        self.nodes = []

        # Update the render window
        self.renderer.GetRenderWindow().Render()

    def create_packet(self, x, y, z, size=1, color=(0, 0, 255), packet_id=None):
        """Create a packet at the specified location."""
        packet_id = packet_id if packet_id else uuid.uuid4()
        packet = Packet(x, y, z, size=size, color=color, packet_id=packet_id)
        packet.add_to_renderer(self.renderer)

        # Store the packet object in the dictionary
        self.packets[packet_id] = packet

    def remove_packet(self, packet_id):
        """Remove the specified packet from the environment."""
        if packet_id in self.packets:
            packet = self.packets[packet_id]
            packet.remove_from_renderer(self.renderer)
            del self.packets[packet_id]

    def update_packet_position(self, packet_id, x, y, z):
        """Update the position of the specified packet."""
        if packet_id in self.packets:
            packet = self.packets[packet_id]
            packet.update_position(x, y, z)

    def setup_renderer(self):
        """Set up the renderer for the visualization."""
        self.renderer.SetBackground(0.5, 0.5, 0.5)
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(0, -500, 200)
        camera.SetFocalPoint(0, 0, 0)
        camera.SetViewUp(0, 0, 1)
        camera.SetClippingRange(1, 1000)

    def get_renderer(self):
        return self.renderer

    def test_view(self):
        """Create the test visualizing view."""
        self.renderer.SetBackground(0.5, 0.5, 1)
        self.create_ground()
        # self.create_building(-100, -100, 0, 50, 100)
        # self.create_building(100, 100, 0, 50, 100)
        # self.create_node(0, 0, 10)
        # self.create_node(-50, 50, 10)
        # self.create_node(50, -50, 10)
        self.renderer.Render()

    def clear_all_packets(self):
        # Iterate through all the packet IDs and remove them
        for packet_id in list(self.packets.keys()):
            self.remove_packet(packet_id)

        # Render the window again to show the changes
        self.renderer.GetRenderWindow().Render()

    def reset_nodes(self):
        # Iterate through all the packet IDs and remove them
        for packet_id in list(self.packets.keys()):
            self.remove_packet(packet_id)

        # Render the window again to show the changes
        self.renderer.GetRenderWindow().Render()

    def clear_all_nodes(self):
        """Remove all nodes from the environment."""
        for node in self.nodes:
            node.remove_from_renderer(renderer=self.renderer)
        self.nodes = []
