import vtk

from api.rendering.rendering_objects.signal_object.signal import Signal


class WifiSignal(Signal):
    def create_wifi_signal_arcs(self, x, y, z, num_arcs=3, arc_thickness=0.5, arc_resolution=50, normal=(1, 0, 0),
                                direction=(0, 0, 1), radius=10):
        self.create_signal_arcs(x, y, z, num_arcs, arc_thickness, arc_resolution, normal, direction, 135, 225, radius)
