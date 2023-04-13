import math

import vtk


class EnvironmentRenderingApi:
    def __init__(self):
        self.renderer = vtk.vtkRenderer()
        self.setup_renderer()
        self.nodes = []
        self.buildings = []

    def create_ground(self):
        """Create a ground plane for the environment."""
        plane = vtk.vtkPlaneSource()
        plane.SetResolution(200, 200)
        plane.SetOrigin(-500, -500, 0)
        plane.SetPoint1(500, -500, 0)
        plane.SetPoint2(-500, 500, 0)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(plane.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0, 1, 0)

        self.renderer.AddActor(actor)

    def create_building(self, x, y, z, width, height):
        """Create a building at the specified location."""
        cube = vtk.vtkCubeSource()
        cube.SetXLength(width)
        cube.SetYLength(width)
        cube.SetZLength(height)
        cube.SetCenter(x, y, z + height / 2)

        cube_mapper = vtk.vtkPolyDataMapper()
        cube_mapper.SetInputConnection(cube.GetOutputPort())

        cube_actor = vtk.vtkActor()
        cube_actor.SetMapper(cube_mapper)
        cube_actor.GetProperty().SetColor(0.5, 0.5, 0.5)

        self.buildings.append(cube_actor)
        self.renderer.AddActor(cube_actor)

    def create_node(self, x, y, z, radius=1):
        """Create a node at the specified location."""
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(radius)
        sphere.SetCenter(x, y, z)
        sphere.SetPhiResolution(50)
        sphere.SetThetaResolution(50)

        sphere_mapper = vtk.vtkPolyDataMapper()
        sphere_mapper.SetInputConnection(sphere.GetOutputPort())

        sphere_actor = vtk.vtkActor()
        sphere_actor.SetMapper(sphere_mapper)
        sphere_actor.GetProperty().SetColor(1, 0, 0)

        self.nodes.append(sphere_actor)
        self.renderer.AddActor(sphere_actor)

    def create_arrow(self, start, end):
        """Create an arrow from start to end."""
        arrow = vtk.vtkArrowSource()
        arrow.Update()

        arrow_mapper = vtk.vtkPolyDataMapper()
        arrow_mapper.SetInputConnection(arrow.GetOutputPort())

        arrow_actor = vtk.vtkActor()
        arrow_actor.SetMapper(arrow_mapper)
        arrow_actor.GetProperty().SetColor(0, 0, 1)

        direction = [end[i] - start[i] for i in range(3)]
        length = math.sqrt(sum([i ** 2 for i in direction]))

        # Set the position of the arrow at the start point of the line
        arrow_actor.SetPosition(start)

        # Calculate the direction and orientation of the arrow
        arrow_actor.RotateWXYZ(math.degrees(math.atan2(math.sqrt(direction[0] ** 2 + direction[1] ** 2), direction[2])),
                               direction[0], direction[1], 0)
        arrow_actor.RotateWXYZ(math.degrees(math.atan2(direction[1], direction[0])), 0, 0, 1)

        arrow_actor.SetScale(length)

        self.renderer.AddActor(arrow_actor)

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
        """Switch to the visualizing view."""
        self.renderer.SetBackground(0.5, 0.5, 1)
        self.create_ground()
        self.create_building(-100, -100, 0, 50, 100)
        self.create_building(100, 100, 0, 50, 100)
        self.create_node(0, 0, 10)
        self.create_node(-50, 50, 10)
        self.create_node(50, -50, 10)
        self.create_arrow((-50, 50, 10), (50, -50, 10))
        self.create_arrow((50, -50, 10), (-50, 50, 10))
        self.renderer.Render()
