import datetime
import time
import uuid

from network_elements.elements import WiredPacket, Node, NodeUpdate, WirelessPacketReception, Broadcaster
from step.step import WiredPacketStep, NodeUpdateStep
from step.step_enum import StepType
from utils.calcUtils import interpolate_coordinates_3D
from utils.manage import get_objects_by_type, get_node_coordinates_by_id


class StepProcessor:
    def __init__(self):
        self.step_types = StepType
        self.substeps = {step_type: [] for step_type in self.step_types}

    def process_steps(self, data):
        node_data = get_objects_by_type(data.content, Node)
        node_update_data = get_objects_by_type(data.content, NodeUpdate)
        p_data = get_objects_by_type(data.content, WiredPacket)
        num_steps = 20  # Number of animation steps

        # Combine node update data and packet data
        combined_data = node_update_data + p_data

        # Sort the combined data by time
        combined_data.sort(key=lambda x: float(x.time) if hasattr(x, 'time') else float(x.first_byte_transmission_time))

        updated_node_data = node_data.copy()

        for item in combined_data:
            if isinstance(item, NodeUpdate):
                # Update the node position
                node = next((node for node in updated_node_data if node.id == item.id), None)
                if node:
                    if item.x and item.y and item.z is not None:
                        node.loc_x, node.loc_y, node.loc_z = item.x, item.y, item.z
                    node_update = NodeUpdateStep(float(item.time), item.id, item.r, item.g, item.b, item.w, item.h,
                                                 item.x, item.y, item.z, item.descr)
                    self.substeps[StepType.NODE_UPDATE].append(node_update)

            elif isinstance(item, WiredPacket):
                packet_id = uuid.uuid4()
                for step in range(num_steps):
                    time_step = float(item.first_byte_transmission_time) + (
                            step * (float(item.first_byte_received_time) - float(item.first_byte_transmission_time)) / (num_steps - 1))

                    x, y, z = interpolate_coordinates_3D(get_node_coordinates_by_id(updated_node_data, item.from_id),
                                                         get_node_coordinates_by_id(updated_node_data, item.to_id), step,
                                                         num_steps)
                    packet_substep = WiredPacketStep(time_step, packet_id, item.from_id, item.to_id, item.first_byte_transmission_time, item.first_byte_received_time,
                                                     item.meta_info, step,
                                                     x, y, z)
                    if packet_substep.from_id != packet_substep.to_id:
                        self.substeps[StepType.WIRED_PACKET].append(packet_substep)
            elif isinstance(item, WirelessPacketReception):
                pass
            elif isinstance(item, Broadcaster):
                pass

        # Combine all step type lists and sort them by time
        all_substeps = []
        for step_type_list in self.substeps.values():
            all_substeps.extend(step_type_list)

        all_substeps.sort(key=lambda x: x.time)
        # testing function - self.display_steps()
        return all_substeps

    def display_steps(self):
        step_duration = datetime.timedelta(seconds=0.5)  # Duration of each step

        # Combine all step type lists and sort them by time
        all_substeps = []
        for step_type_list in self.substeps.values():
            all_substeps.extend(step_type_list)

        all_substeps.sort(key=lambda x: x.time)

        for substep in all_substeps:
            print(f"Time: {substep.time}")

            if isinstance(substep, WiredPacketStep):
                print(
                    f"  packetId: {substep.packet_id} fId: {substep.from_id} tId: {substep.to_id} fbTx: {substep.first_byte_transmission_time} fbRx: {substep.first_byte_received_time}")
                print(f"  step_n: {substep.step_number}")
                print(f"  x: {substep.loc_x} y: {substep.loc_y} z: {substep.loc_z}")
                print(f"  Meta-info: {substep.meta_info}")
            elif isinstance(substep, NodeUpdateStep):
                print(f"  node_id: {substep.node_id}")
                print(f"  r: {substep.red} g: {substep.green} b: {substep.blue}")
                print(f"  w: {substep.width} h: {substep.height}")
                print(f"  x: {substep.loc_x} y: {substep.loc_y} z: {substep.loc_z}")
                print(f"  description: {substep.description}")

            print()
            time.sleep(step_duration.total_seconds())
