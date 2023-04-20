from PyQt5.QtCore import QCoreApplication, QTimer

from network_elements.elements import Node
from step.step_enum import StepType
from utils.manage import get_objects_by_type, get_rendering_node_by_id


class AnimationApi:
    def __init__(self, renderer_api):
        self.renderer_api = renderer_api
        self.data = None
        self.substeps = []
        self.current_step = 0
        self.delay = 0
        self.steps_per_event = 1
        self.is_paused = False
        self.max_steps_callback = None
        self.steps_update_callback = None
        self.control_update_callback = None
        self.progress_bar_update_callback = None
        self.progress_bar_maximum_callback = None
        self.animation_started = False
        self.timer_step = QTimer()

    def set_data(self, data):
        self.data = data

    def set_control_update_callback(self, callback):
        self.control_update_callback = callback

    def prepare_animation(self):
        if self.data and self.data.content:
            nodes = get_objects_by_type(self.data.content, Node)
            for node in nodes:
                self.renderer_api.create_node(x=node.loc_x, y=node.loc_y, z=node.loc_z, id=node.id,
                                              description="Node " + node.id)
            self.renderer_api.renderer.GetRenderWindow().Render()

    def animate_substeps(self):
        if not self.animation_started:
            self.animation_started = True
            self.timer_step.timeout.connect(self.run_single_step)
            self.start_timer()

    def run_single_step(self):
        steps_executed = 0
        render_every_n_steps = 10  # Adjust this value based on your requirements

        while self.current_step < len(self.substeps) and not self.is_paused:
            step = self.substeps[self.current_step]
            self.handle_step(step)
            self.current_step += 1

            if self.control_update_callback:
                self.control_update_callback(
                    f"Step {self.current_step} / {len(self.substeps)}",
                    f"Time {step.time}",
                    self.current_step,
                    len(self.substeps),
                )
            if self.steps_update_callback:
                self.steps_update_callback(self.current_step)
            if steps_executed % render_every_n_steps == 0:
                self.renderer_api.renderer.GetRenderWindow().Render()
                QCoreApplication.processEvents()  # Process events during animation

            steps_executed += 1

            if steps_executed >= self.steps_per_event:
                break

        self.start_timer()

    def handle_step(self, step):
        match step.type:
            case StepType.WIRED_PACKET:
                self.handle_packet_step(step)
            case StepType.NODE_UPDATE:
                self.handle_node_update(step)

    def handle_packet_step(self, step):
        packet_id = step.packet_id
        if step.step_number == 0:
            x, y, z = step.loc_x, step.loc_y, step.loc_z
            self.renderer_api.create_packet(x, y, z, packet_id=packet_id)
        elif step.step_number == 19 and packet_id in self.renderer_api.packets:
            if packet_id in self.renderer_api.packets:
                self.renderer_api.remove_packet(packet_id)
        # Update the position of the packet for intermediate steps
        elif packet_id in self.renderer_api.packets:
            x, y, z = step.loc_x, step.loc_y, step.loc_z
            self.renderer_api.update_packet_position(packet_id, x, y, z)

    def handle_node_update(self, step):
        # Find the node with the matching ID
        node = get_rendering_node_by_id(self.renderer_api.nodes, step.node_id)
        node.update_attributes(step, self.renderer_api.renderer)

    def start_timer(self):
        self.timer_step.start(self.delay)

    def stop_timer(self):
        self.timer_step.stop()

    def pause_unpause_animation(self):
        self.is_paused = not self.is_paused
        if not self.is_paused:
            self.start_timer()
        else:
            self.stop_timer()

    def pause_animation(self):
        self.is_paused = True
        self.stop_timer()

    def unpause_animation(self):
        self.is_paused = False
        self.start_timer()

    def reset_animation(self):
        self.current_step = 0
        self.clear_vtk_window()

    def clear_vtk_window(self):
        self.renderer_api.clear_all_packets()
        self.renderer_api.clear_all_nodes()
        self.prepare_animation()
        if self.control_update_callback:
            self.control_update_callback(f"Step {self.current_step} / {len(self.substeps)}", "Time 0",
                                         self.current_step, len(self.substeps))

    def update_delay(self, new_delay):
        self.delay = new_delay

    def update_steps_per_event(self, new_steps_per_event):
        self.steps_per_event = new_steps_per_event

    def set_update_steps_callback(self, callback):
        self.steps_update_callback = callback

    def set_current_step(self, new_step):
        self.current_step = new_step
        self.clear_vtk_window()
        for i in range(new_step):
            if i < len(self.substeps):
                step = self.substeps[i]
                self.handle_step(step)
        self.renderer_api.renderer.GetRenderWindow().Render()

    def set_max_steps_callback(self, callback):
        self.max_steps_callback = callback

    def set_substeps(self, substeps):
        self.substeps = substeps
        if self.max_steps_callback:
            self.max_steps_callback(len(self.substeps))
