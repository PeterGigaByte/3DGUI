import numpy as np
import vtk


class Signal:
    def __init__(self, renderer):
        self.renderer = renderer

    def create_arc_points(self, radius, start_angle, end_angle, num_points=50):
        angles = np.linspace(start_angle, end_angle, num_points)
        x = radius * np.cos(np.radians(angles))
        y = radius * np.sin(np.radians(angles))
        points = np.column_stack((x, y, np.zeros_like(x)))
        return points

    def create_signal_arcs(self, x, y, z, num_arcs, arc_thickness, arc_resolution, normal, direction, start_angle,
                           end_angle, radius):
        arc_list = []
        for i in range(1, num_arcs + 1):
            points = vtk.vtkPoints()

            arc_points = self.create_arc_points(radius, start_angle, end_angle, arc_resolution)

            for point in arc_points:
                points.InsertNextPoint(point)

            spline = vtk.vtkParametricSpline()
            spline.SetPoints(points)

            spline_function = vtk.vtkParametricFunctionSource()
            spline_function.SetParametricFunction(spline)
            spline_function.SetUResolution(arc_resolution)
            spline_function.Update()

            tube_filter = vtk.vtkTubeFilter()
            tube_filter.SetInputConnection(spline_function.GetOutputPort())
            tube_filter.SetRadius(arc_thickness)
            tube_filter.SetNumberOfSides(20)
            tube_filter.CappingOn()
            tube_filter.Update()

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(tube_filter.GetOutput())

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(0, 0, 1)
            actor.SetPosition(x, y, z)

            # Calculate the angle between the z-axis and the normal
            angle_normal = np.arccos(np.dot(normal, (0, 0, 1)) / np.linalg.norm(normal)) * 180 / np.pi
            # Calculate the angle between the z-axis and the direction
            angle_direction = np.arccos(np.dot(direction, (0, 0, 1)) / np.linalg.norm(direction)) * 180 / np.pi

            # Calculate the rotation axis for the normal and direction
            rotation_axis_normal = np.cross((0, 0, 1), normal)
            rotation_axis_direction = np.cross((0, 0, 1), direction)

            # Rotate the actor using the calculated angles and rotation axes
            actor.RotateWXYZ(angle_normal, *rotation_axis_normal)
            actor.RotateWXYZ(angle_direction, *rotation_axis_direction)

            self.renderer.AddActor(actor)
            arc_list.append(actor)

        self.renderer.GetRenderWindow().Render()
        return arc_list


