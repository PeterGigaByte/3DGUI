"""
This element describes a packet_object over wired links being transmitted at some node_object and received at another.

The reception details are described in its associated rx element
"""
from step.step_enum import StepType


class Step:
    def __init__(self, time, step_type):
        self.time = time
        self.type = step_type

    def process(self):
        pass


class WiredPacketStep(Step):
    def __init__(self, time, packet_id, from_id, to_id, first_byte_transmission_time, first_byte_received_time,
                 meta_info,
                 step_number, loc_x, loc_y, loc_z):
        super().__init__(time, StepType.WIRED_PACKET)
        self.packet_id = packet_id
        self.from_id = from_id
        self.to_id = to_id
        self.first_byte_transmission_time = first_byte_transmission_time
        self.first_byte_received_time = first_byte_received_time
        self.meta_info = meta_info
        self.step_number = step_number
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.loc_z = loc_z


class NodeUpdateStep(Step):
    def __init__(self, time, node_id, description, red, green, blue, width, height, loc_x, loc_y, loc_z=0):
        super().__init__(time, StepType.NODE_UPDATE)
        self.node_id = node_id
        self.red = red
        self.green = green
        self.blue = blue
        self.width = width
        self.height = height
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.loc_z = loc_z
        self.description = description


class BroadcastStep(Step):
    def __init__(self, broadcast_id, time, loc_x, loc_y, radius, step_number, loc_z=0):
        super().__init__(time, StepType.BROADCAST)
        self.broadcast_id = broadcast_id
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.loc_z = loc_z
        self.radius = radius
        self.step_number = step_number


class WirelessPacketReceptionStep(Step):
    def __init__(self, wireless_packet_id, time, loc_x, loc_y, broadcast_loc_x, broadcast_loc_y, radius, step_number, loc_z=0, broadcast_loc_z=0):
        super().__init__(time, StepType.WIRELESS_PACKET_RECEPTION)
        self.wireless_packet_id = wireless_packet_id
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.loc_z = loc_z
        self.broadcast_loc_x = broadcast_loc_x
        self.broadcast_loc_y = broadcast_loc_y
        self.broadcast_loc_z = broadcast_loc_z
        self.radius = radius
        self.step_number = step_number

