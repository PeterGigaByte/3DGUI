"""
This element describes a packet over wired links being transmitted at some node and received at another.

The reception details are described in its associated rx element
"""
from step.step_enum import StepType


class Step:
    def __init__(self, time, type):
        self.time = time
        self.type = type

    def process(self):
        pass


class PacketStep(Step):
    def __init__(self, time, packet_id, f_id, t_id, fb_tx, fb_rx, meta_info, step_n, x, y, z):
        super().__init__(time, StepType.WIRED_PACKET)
        self.packet_id = packet_id
        self.f_id = f_id
        self.t_id = t_id
        self.fb_tx = fb_tx
        self.fb_rx = fb_rx
        self.meta_info = meta_info
        self.step_n = step_n
        self.x = x
        self.y = y
        self.z = z

    def process(self):
        # Process packet step
        pass


class NodeUpdateStep(Step):
    def __init__(self, time, node_id, r, g, b, w, h, x, y, z, descr):
        super().__init__(time, StepType.NODE_UPDATE)
        self.node_id = node_id
        self.r = r
        self.g = g
        self.b = b
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.z = z
        self.descr = descr

    def process(self):
        # Process packet step
        pass
