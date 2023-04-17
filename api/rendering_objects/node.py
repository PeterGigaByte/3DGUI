import uuid

import vtk

from utils.renderingUtils import normalize_rgb


class Node:
    def __init__(self, x, y, z, radius=1, description="Node", node_color=(255, 0, 0), label_color=(255, 255, 255), node_id=None):
        self.node_id = node_id if node_id else uuid.uuid4()
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.description = description
        self.node_color = node_color
        self.label_color = label_color
        self.sphere_actor = self.create_sphere_actor()
        self.text_actor = self.create_text_actor()

    def create_sphere_actor(self):
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(self.radius)
        sphere.SetCenter(self.x, self.y, self.z)
        sphere.SetPhiResolution(50)
        sphere.SetThetaResolution(50)

        sphere_mapper = vtk.vtkPolyDataMapper()
        sphere_mapper.SetInputConnection(sphere.GetOutputPort())

        sphere_actor = vtk.vtkActor()
        sphere_actor.SetMapper(sphere_mapper)
        sphere_actor.GetProperty().SetColor(*normalize_rgb(self.node_color))

        return sphere_actor

    def create_text_actor(self):
        # Create a text label
        text_source = vtk.vtkVectorText()
        text_source.SetText(f"{self.description}\n({self.x}, {self.y}, {self.z})")

        text_mapper = vtk.vtkPolyDataMapper()
        text_mapper.SetInputConnection(text_source.GetOutputPort())

        text_actor = vtk.vtkFollower()
        text_actor.SetMapper(text_mapper)
        text_actor.GetProperty().SetColor(*normalize_rgb(self.label_color))  # Normalize the label color
        text_actor.SetScale(0.5)  # Set the scale of the text
        text_actor.SetPosition(self.x, self.y - 2.5 * self.radius, self.z)  # Adjust the position based on your object

        return text_actor

    def add_to_renderer(self, renderer):
        renderer.AddActor(self.sphere_actor)
        renderer.AddActor(self.text_actor)
        self.text_actor.SetCamera(renderer.GetActiveCamera())  # Set the camera for the vtkFollower

    def remove_from_renderer(self, renderer):
        renderer.RemoveActor(self.sphere_actor)
        renderer.RemoveActor(self.text_actor)

    def update_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.sphere_actor.SetPosition(self.x, self.y, self.z)
        self.text_actor.SetPosition(self.x, self.y - 2.5 * self.radius, self.z)
