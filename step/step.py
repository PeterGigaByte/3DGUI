"""
This element describes a packet over wired links being transmitted at some node and received at another.

The reception details are described in its associated rx element
"""


class WiredPacketAnimationStep:
    def __init__(self, packet_id, time_step, f_id, t_id, fb_tx, fb_rx, meta_info, step, x, y, z):
        self.packetId = packet_id,
        self.time = time_step,
        self.fId = f_id,
        self.tId = t_id,
        self.fbTx = fb_tx,
        self.fbRx = fb_rx,
        self.meta_info = meta_info,
        self.stepN = step,
        self.locX = x,
        self.locY = y,
        self.locZ = z


"""
This element describes a packet over wireless links being transmitted at some node and received at another.

The reception details are described in its associated rx element.
"""


class WirelessPacketAnimationStep:
    def __init__(self, packet_id, time_step, f_id, t_id, fb_tx, fb_rx, meta_info, step, x, y, z):
        self.packetId = packet_id,
        self.time = time_step,
        self.fId = f_id,
        self.tId = t_id,
        self.fbTx = fb_tx,
        self.fbRx = fb_rx,
        self.meta_info = meta_info,
        self.stepN = step,
        self.locX = x,
        self.locY = y,
        self.locZ = z


class NodeUpdateStep:
    def __init__(self, type, time, node_id, red, green, blue, width, height, loc_x, loc_y, loc_z, descr):
        self.type = type
        self.time = time
        self.id = node_id
        self.red = red
        self.green = green
        self.blue = blue
        self.width = width
        self.height = height
        self.locX = loc_x
        self.locY = loc_y
        self.locZ = loc_z
        self.descr = descr
