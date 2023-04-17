import datetime
import time
import uuid

from network_elements.elements import P, Node
from utils.calcUtils import interpolate_coordinates_3D
from utils.manage import get_objects_by_type, get_node_coor_by_id


class StepProcessor:
    def __init__(self):
        self.substeps = []

    def process_steps(self, data):
        node_data = get_objects_by_type(data.content, Node)
        p_data = get_objects_by_type(data.content, P)
        num_steps = 20  # Number of animation steps

        for p in p_data:
            packet_id = uuid.uuid4()
            for step in range(num_steps):
                time_step = float(p.fb_tx) + (
                        step * (float(p.fb_rx) - float(p.fb_tx)) / (num_steps - 1))
                x, y, z = interpolate_coordinates_3D(get_node_coor_by_id(node_data, p.f_id),
                                                     get_node_coor_by_id(node_data, p.t_id), step, num_steps)
                substep = {
                    'packetId': packet_id,
                    'time': time_step,
                    'fId': p.f_id,
                    'tId': p.t_id,
                    'fbTx': p.fb_tx,
                    'fbRx': p.fb_rx,
                    'meta_info': p.meta_info,
                    'stepN': step,
                    'locX': x,
                    'locY': y,
                    'locZ': z
                }
                if substep["fId"] != substep["tId"]:
                    self.substeps.append(substep)

        self.substeps.sort(key=lambda x: x['time'])
        return self.substeps

    def display_packets(self):
        step_duration = datetime.timedelta(seconds=0.5)  # Duration of each step
        for substep in self.substeps:
            print(f"Time: {substep['time']}")
            print(
                f"  packetId: {substep['packetId']} fId: {substep['fId']} tId: {substep['tId']} fbTx: {substep['fbTx']} fbRx: {substep['fbRx']}")
            print(f"  step: {substep['stepN']}")
            print(f"  x: {substep['locX']} y: {substep['locY']} z: {substep['locZ']}")
            print(f"  Meta-info: {substep['meta_info']}")
            print()
            time.sleep(step_duration.total_seconds())
