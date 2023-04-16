import vtk


def normalize_rgb(rgb):
    return tuple(channel / 255.0 for channel in rgb)


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

    def create_node(self, x, y, z, radius=1, description="Node", node_color=(255, 0, 0), label_color=(255, 255, 255)):
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
        sphere_actor.GetProperty().SetColor(*normalize_rgb(node_color))

        # Create a text label
        text_source = vtk.vtkVectorText()
        text_source.SetText(f"{description}\n({x}, {y}, {z})")

        text_mapper = vtk.vtkPolyDataMapper()
        text_mapper.SetInputConnection(text_source.GetOutputPort())

        text_actor = vtk.vtkFollower()
        text_actor.SetMapper(text_mapper)
        text_actor.GetProperty().SetColor(*normalize_rgb(label_color))  # Normalize the label color
        text_actor.SetScale(0.5)  # Set the scale of the text
        text_actor.SetPosition(x, y - 2.5 * radius, z)  # Adjust the position based on your object
        text_actor.SetCamera(self.renderer.GetActiveCamera())  # Set the camera for the vtkFollower

        self.nodes.append((sphere_actor, text_actor))
        self.renderer.AddActor(sphere_actor)
        self.renderer.AddActor(text_actor)

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
        #self.create_building(-100, -100, 0, 50, 100)
        #self.create_building(100, 100, 0, 50, 100)
        #self.create_node(0, 0, 10)
        #self.create_node(-50, 50, 10)
        #self.create_node(50, -50, 10)
        self.renderer.Render()
