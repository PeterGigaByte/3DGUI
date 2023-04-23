import uuid

import vtk

from utils.renderingUtils import normalize_rgb


class Node:
    def __init__(self, x, y, z, radius=1, description="Node", node_color=(255, 0, 0), label_color=(255, 255, 255),
                 node_id=None):
        self.node_id = node_id if node_id else uuid.uuid4()
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.description = description
        self.node_color = node_color
        self.label_color = label_color
        self.text_source = vtk.vtkVectorText()
        self.sphere = vtk.vtkSphereSource()
        self.sphere_actor = self.create_sphere_actor()
        self.text_actor = self.create_text_actor()

    def create_sphere_actor(self):
        self.update_sphere()
        sphere_mapper = vtk.vtkPolyDataMapper()
        sphere_mapper.SetInputConnection(self.sphere.GetOutputPort())

        sphere_actor = vtk.vtkActor()
        sphere_actor.SetMapper(sphere_mapper)
        sphere_actor.GetProperty().SetColor(*normalize_rgb(self.node_color))

        return sphere_actor

    def update_sphere(self):
        self.sphere.SetRadius(self.radius)
        self.sphere.SetCenter(self.x, self.y, self.z)
        self.sphere.SetPhiResolution(50)
        self.sphere.SetThetaResolution(50)
        self.sphere.Modified()

    def create_text_actor(self):
        text_mapper = vtk.vtkPolyDataMapper()
        text_mapper.SetInputConnection(self.text_source.GetOutputPort())

        text_actor = vtk.vtkFollower()
        text_actor.SetMapper(text_mapper)
        text_actor.GetProperty().SetColor(*normalize_rgb(self.label_color))
        text_actor.SetScale(0.5)
        self.update_text_actor(text_actor)

        return text_actor

    def update_text_actor(self, text_actor):
        self.text_source.SetText(f"{self.description}\n({round(self.x)}, {round(self.y)}, {round(self.z)})")
        self.text_source.Modified()
        text_actor.SetPosition(self.x, self.y - 2.5 * self.radius, self.z)

    def add_to_renderer(self, renderer):
        renderer.AddActor(self.sphere_actor)
        renderer.AddActor(self.text_actor)
        self.text_actor.SetCamera(renderer.GetActiveCamera())

    def remove_from_renderer(self, renderer):
        renderer.RemoveActor(self.sphere_actor)
        renderer.RemoveActor(self.text_actor)

    def update_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.sphere_actor.SetPosition(self.x, self.y, self.z)
        self.update_text_actor(self.text_actor)

    def update_attributes(self, node, renderer):
        if node.loc_x is not None and node.loc_y is not None and node.loc_z is not None:
            self.x = float(node.loc_x)
            self.y = float(node.loc_y)
            self.z = float(node.loc_z)
            self.update_sphere()
            self.update_text_actor(self.text_actor)

        if node.description is not None:
            self.description = node.description
            self.update_text_actor(self.text_actor)
        if node.red is not None and node.green is not None and node.blue is not None:
            self.node_color = (float(node.red), float(node.green), float(node.blue))
            self.sphere_actor.GetProperty().SetColor(*normalize_rgb(self.node_color))
        if renderer:
            self.text_actor.SetCamera(renderer.GetActiveCamera())
            renderer.Render()  # Force a render to update the changes