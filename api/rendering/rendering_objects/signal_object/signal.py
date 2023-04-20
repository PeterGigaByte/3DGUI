import numpy as np
import vtk


class Signal:
    def __init__(self, renderer):
        self.renderer = renderer

    def create_arc_points(self, radius, start_angle, end_angle, spacing, num_points=50):
        angles = np.linspace(start_angle, end_angle, num_points)
        x = (radius + spacing) * np.cos(np.radians(angles))
        y = (radius + spacing) * np.sin(np.radians(angles))
        points = np.column_stack((x, y, np.zeros_like(x)))
        return points

    def create_signal_arcs(self, x, y, z, num_arcs, arc_thickness, arc_resolution, normal, direction, start_angle, end_angle, spacing=0, first_arc_distance=10):
        arc_list = []

        for i in range(1, num_arcs + 1):
            points = vtk.vtkPoints()

            arc_points = self.create_arc_points(i * 10 + spacing * (i - 1) + first_arc_distance * (i == 1), start_angle, end_angle, arc_resolution)

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
            actor.RotateWXYZ(90, *normal)
            actor.RotateWXYZ(90, *direction)
            self.renderer.AddActor(actor)
            arc_list.append(actor)

        self.renderer.GetRenderWindow().Render()