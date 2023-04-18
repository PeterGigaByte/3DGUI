"""
This element describes a packet over wired links being transmitted at some node and received at another.

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
    def __init__(self, time, node_id, red, green, blue, width, height, loc_x, loc_y, loc_z, description):
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
    def __init__(self, time):
        super().__init__(time, StepType.BROADCAST)


class WirelessPacketReceptionStep(Step):
    def __init__(self, time):
        super().__init__(time, StepType.WIRELESS_PACKET_RECEPTION)
