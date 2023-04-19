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
        """
        Processes the animation steps for the provided data and returns a sorted list of all substeps.

        Args:
        - data: an object containing the data to process

        Returns:
        - A sorted list of all substeps for the provided data
        """
        # Get the node data, node update data, and wired packet data from the content of the provided data
        node_data = get_objects_by_type(data.content, Node)
        node_update_data = get_objects_by_type(data.content, NodeUpdate)
        wired_packet_data = get_objects_by_type(data.content, WiredPacket)

        # Set the number of steps to interpolate between each substep for wired packets
        num_steps = 20

        # Combine the node update data and wired packet data
        combined_data = node_update_data + wired_packet_data

        # Sort the combined data by time
        combined_data.sort(key=lambda x: float(x.time) if hasattr(x, 'time') else float(x.first_byte_transmission_time))

        # Create a copy of the node data to update
        updated_node_data = node_data.copy()

        # Loop through the combined data and generate substeps for each item
        for item in combined_data:
            if isinstance(item, NodeUpdate):
                # If the item is a NodeUpdate, update the position of the corresponding node and add a NodeUpdateStep
                self.update_node_position(item, updated_node_data)
            elif isinstance(item, WiredPacket):
                # If the item is a WiredPacket, generate substeps for the packet and add WiredPacketStep objects
                self.generate_wired_packet_substeps(item, num_steps, updated_node_data)
            elif isinstance(item, WirelessPacketReception):
                # If the item is a WirelessPacketReception, do nothing (for now)
                pass
            elif isinstance(item, Broadcaster):
                # If the item is a Broadcaster, do nothing (for now)
                pass

        # Combine all substeps for each step type and sort them by time
        all_substeps = []
        for step_type_list in self.substeps.values():
            all_substeps.extend(step_type_list)
        all_substeps.sort(key=lambda x: x.time)

        # Return the sorted list of all substeps
        return all_substeps

    def display_steps(self):
        """
        Displays the substeps in the substeps dictionary in sorted order, with a delay between each step.

        Args:
        - None

        Returns:
        - None
        """
        # Set the duration of each step to 0.5 seconds
        step_duration = datetime.timedelta(seconds=0.5)

        # Combine all substeps for each step type and sort them by time
        all_substeps = []
        for step_type_list in self.substeps.values():
            all_substeps.extend(step_type_list)
        all_substeps.sort(key=lambda x: x.time)

        # Loop through each substep and print its information with a delay between steps
        for substep in all_substeps:
            print(f"Time: {substep.time}")

            if isinstance(substep, WiredPacketStep):
                # If the substep is a WiredPacketStep, print its information
                print(
                    f"  packetId: {substep.packet_id} fId: {substep.from_id} tId: {substep.to_id} fbTx: {substep.first_byte_transmission_time} fbRx: {substep.first_byte_received_time}")
                print(f"  step_n: {substep.step_number}")
                print(f"  x: {substep.loc_x} y: {substep.loc_y} z: {substep.loc_z}")
                print(f"  Meta-info: {substep.meta_info}")
            elif isinstance(substep, NodeUpdateStep):
                # If the substep is a NodeUpdateStep, print its information
                print(f"  node_id: {substep.node_id}")
                print(f"  r: {substep.red} g: {substep.green} b: {substep.blue}")
                print(f"  w: {substep.width} h: {substep.height}")
                print(f"  x: {substep.loc_x} y: {substep.loc_y} z: {substep.loc_z}")
                print(f"  description: {substep.description}")

            print()

            # Delay for the duration of a step
            time.sleep(step_duration.total_seconds())

    def create_substeps(self, num_steps, item, updated_data, get_coordinates_by_id, interpolate_coordinates, create_step, start_time, end_time):
        substeps = []

        for step in range(num_steps):
            # Calculate the time step for the current step
            time_step = float(start_time) + (
                    step * (float(end_time) - float(start_time)) / (num_steps - 1))

            # Get the source and destination coordinates using the provided function
            src_coordinates = get_coordinates_by_id(updated_data, item.from_id)
            dst_coordinates = get_coordinates_by_id(updated_data, item.to_id)

            # Interpolate the coordinates for the current step
            x, y, z = interpolate_coordinates(src_coordinates, dst_coordinates, step, num_steps)

            # Create a new step object using the provided function
            substep = create_step(time_step, item, step, x, y, z)

            # Add the created step object to the list of substeps
            substeps.append(substep)

        return substeps

    def generate_wired_packet_substeps(self, item, num_steps, updated_node_data):
        """
        Generates substeps for a wired packet based on the number of steps specified.

        Args:
        - item: an object representing the wired packet
        - num_steps: the number of steps to interpolate
        - updated_node_data: a dictionary containing updated node data

        Returns:
        - A list of WiredPacketStep objects representing the substeps of the wired packet
        """
        # Generate a unique packet ID
        packet_id = uuid.uuid4()

        # Loop through the number of steps specified
        for step in range(num_steps):
            # Calculate the time step based on the transmission and reception times
            time_step = float(item.first_byte_transmission_time) + (
                    step * (float(item.first_byte_received_time) - float(item.first_byte_transmission_time)) / (
                        num_steps - 1))

            # Interpolate the 3D coordinates between the source and destination nodes
            x, y, z = interpolate_coordinates_3D(get_node_coordinates_by_id(updated_node_data, item.from_id),
                                                 get_node_coordinates_by_id(updated_node_data, item.to_id), step,
                                                 num_steps)

            # Create a WiredPacketStep object for this substep
            packet_substep = WiredPacketStep(time_step, packet_id, item.from_id, item.to_id,
                                             item.first_byte_transmission_time, item.first_byte_received_time,
                                             item.meta_info, step, x, y, z)

            # Append the WiredPacketStep object to the list of substeps
            if packet_substep.from_id != packet_substep.to_id:
                self.substeps[StepType.WIRED_PACKET].append(packet_substep)

    def update_node_position(self, item, updated_node_data):
        """
        Updates the position of a node in updated_node_data and adds a NodeUpdateStep to the substeps.

        Args:
        - item: an object representing the updated node position
        - updated_node_data: a dictionary containing updated node data

        Returns:
        - None
        """
        # Find the node with the matching ID in updated_node_data
        node = next((node for node in updated_node_data if node.id == item.id), None)

        # If the node exists, update its position
        if node:
            if item.x and item.y and item.z is not None:
                node.loc_x, node.loc_y, node.loc_z = item.x, item.y, item.z

            # Create a NodeUpdateStep object for this update
            node_update = NodeUpdateStep(time=float(item.time), node_id=item.id, red=item.r, green=item.g, blue=item.b,
                                         width=item.w, height=item.h,
                                         loc_x=item.x, loc_y=item.y, loc_z=item.z, description=item.descr)

            # Append the NodeUpdateStep object to the list of substeps
            self.substeps[StepType.NODE_UPDATE].append(node_update)

