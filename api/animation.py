import vtk

from network_elements.elements import Node
from utils.manage import get_objects_by_type


class AnimationApi:
    def __init__(self, renderer_api):
        self.timer_id = None
        self.renderer_api = renderer_api
        self.data = None
        self.substeps = []
        self.current_substep = 0
        self.delay = 1000  # Animation delay in milliseconds
        self.is_paused = False
        self.control_update_callback = None
        self.progress_bar_update_callback = None
        self.progress_bar_maximum_callback = None

    def set_data(self, data):
        self.data = data

    def set_control_update_callback(self, callback):
        self.control_update_callback = callback

    def set_substeps(self, substeps):
        self.substeps = substeps

    def prepare_animation(self):
        nodes = get_objects_by_type(self.data.content, Node)
        for node in nodes:
            self.renderer_api.create_node(int(node.loc_x), int(node.loc_y), int(node.loc_z))
        self.renderer_api.renderer.GetRenderWindow().Render()

    def animate_substeps(self):
        interactor = self.renderer_api.renderer.GetRenderWindow().GetInteractor()
        interactor.CreateRepeatingTimer(self.delay)
        interactor.AddObserver(vtk.vtkCommand.TimerEvent, self.on_timer)
        self.timer_id = interactor.CreateRepeatingTimer(self.delay)

    def on_timer(self, obj, event):
        if not self.is_paused:
            if self.current_substep < len(self.substeps):
                substep = self.substeps[self.current_substep]
                self.handle_step(substep)
                self.current_substep += 1

                # Call the callback function if set
                if self.control_update_callback:
                    self.control_update_callback(f"Step {self.current_substep} / {len(self.substeps)}", f"Time {substep['time']}", self.current_substep, len(self.substeps))
            else:
                # Stop the timer if there are no more substeps
                obj.DestroyTimer()

    def handle_step(self, substep):
        packet_id = substep['packetId']
        if substep['stepN'] == 0:
            x, y, z = substep['locX'], substep['locY'], substep['locZ']
            self.renderer_api.create_packet(x, y, z, packet_id=packet_id)
        elif substep['stepN'] == 19 and packet_id in self.renderer_api.packets:
            if packet_id in self.renderer_api.packets:
                self.renderer_api.remove_packet(packet_id)
        # Update the position of the packet for intermediate steps
        elif packet_id in self.renderer_api.packets:
            x, y, z = substep['locX'], substep['locY'], substep['locZ']
            self.renderer_api.update_packet_position(packet_id, x, y, z)
            self.renderer_api.renderer.GetRenderWindow().Render()

    def pause_animation(self):
        self.is_paused = not self.is_paused

    def update_delay(self, new_delay):
        self.delay = new_delay
        interactor = self.renderer_api.renderer.GetRenderWindow().GetInteractor()
        interactor.DestroyTimer(self.timer_id)
        self.timer_id = interactor.CreateRepeatingTimer(self.delay)

