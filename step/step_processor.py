import datetime
import time
import uuid

from network_elements.elements import WiredPacket, Node, NodeUpdate, WirelessPacketReception, Broadcaster
from step.step import WiredPacketStep, NodeUpdateStep, BroadcastStep, WirelessPacketReceptionStep
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
        # Get the node_object data, node_object update data, and wired packet_object data from the content of the
        # provided data
        node_data = get_objects_by_type(data.content, Node)
        node_update_data = get_objects_by_type(data.content, NodeUpdate)
        wired_packet_data = get_objects_by_type(data.content, WiredPacket)
        broadcaster_data = get_objects_by_type(data.content, Broadcaster)
        wireless_packet_data = get_objects_by_type(data.content, WirelessPacketReception)

        # Set the number of steps to interpolate between each substep for wired packets
        num_steps_wired_packet_animation = 20
        # broadcast step parameters
        num_steps_broadcast_transmission = 4
        # wireless packet_object reception step parameters
        num_steps_wireless_packet_reception = 4
        # first radius
        radius_constant = 5
        end_time_constant = 0.000010

        # Combine the node_object update data and wired packet_object data
        combined_data = node_update_data + wired_packet_data + broadcaster_data + wireless_packet_data

        # Sort the combined data by time
        combined_data.sort(key=lambda x: float(x.time) if hasattr(x, 'time') else (
            float(x.first_byte_transmission_time) if hasattr(x, 'first_byte_transmission_time') else float(
                x.first_byte_received_time)))

        # Create a copy of the node_object data to update
        updated_node_data = node_data.copy()
        wireless_packet_max_time_map = {}

        for item in wireless_packet_data:
            if item.unique_id not in wireless_packet_max_time_map or item.first_byte_received_time \
                    > wireless_packet_max_time_map[item.unique_id]:
                wireless_packet_max_time_map[item.unique_id] = item.first_byte_received_time
        broadcaster_transmitted = {}
        # Loop through the combined data and generate substeps for each item
        for item in combined_data:
            if isinstance(item, NodeUpdate):
                # If the item is a NodeUpdate, update the position of the corresponding node_object and add a NodeUpdateStep
                # Find the node_object with the matching ID in updated_node_data
                node = next((node for node in updated_node_data if node.id == item.id), None)

                # If the node_object exists, update its position
                if node:
                    if item.x and item.y and item.z is not None:
                        node.loc_x, node.loc_y, node.loc_z = item.x, item.y, item.z
                self.update_node_position(item)
            elif isinstance(item, WiredPacket):
                # If the item is a WiredPacket, generate substeps for the packet_object and add WiredPacketStep objects
                self.generate_wired_packet_substeps(item, num_steps_wired_packet_animation, updated_node_data)
            elif isinstance(item, Broadcaster):
                # If the item is a Broadcaster, do nothing (for now)
                end_time = None
                try:
                    end_time = wireless_packet_max_time_map[item.unique_id]
                except KeyError:
                    print("End time was not defined. Constant will be used")
                self.generate_transmitter_broadcast_substeps(item, num_steps_broadcast_transmission,
                                                             end_time,
                                                             radius_constant, updated_node_data, end_time_constant)
                broadcaster_transmitted[item.unique_id] = item
                pass
            elif isinstance(item, WirelessPacketReception):
                # If the item is a WirelessPacketReception, do nothing (for now)
                self.generate_wireless_packet_reception_substeps(item, num_steps_wireless_packet_reception,
                                                                 broadcaster_transmitted[item.unique_id],
                                                                 radius_constant, updated_node_data)

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

    def generate_wired_packet_substeps(self, item, num_steps, updated_node_data):
        """
        Generates substeps for a wired packet_object based on the number of steps specified.

        Args:
        - item: an object representing the wired packet_object
        - num_steps: the number of steps to interpolate
        - updated_node_data: a dictionary containing updated node_object data

        Returns:
        - A list of WiredPacketStep objects representing the substeps of the wired packet_object
        """
        # Generate a unique packet_object ID
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

    def generate_transmitter_broadcast_substeps(self, broadcaster, num_steps, end_time, radius_constant, updated_node_data, end_time_constant):
        broadcast_substeps = []
        if end_time is None:
            end_time = float(broadcaster.first_byte_transmission_time) + end_time_constant
        # Get the node_object associated with the broadcaster using the from_id (f_id)
        node = next((node for node in updated_node_data if node.id == broadcaster.from_id), None)

        if not node:
            # If the node is not found, return an empty list
            return

        # Calculate the time step for each substep
        time_step = (float(end_time) - float(broadcaster.first_byte_transmission_time)) / (num_steps - 1)

        # Generate the substeps
        for step in range(num_steps):
            # Calculate the time for the current substep
            substep_time = float(broadcaster.first_byte_transmission_time) + step * time_step
            radius = radius_constant * step
            # Create a BroadcastStep object for the current substep
            broadcast_substep = BroadcastStep(
                time=substep_time, loc_x=node.loc_x,
                loc_y=node.loc_y, loc_z=node.loc_z,
                radius=radius, step_number=step)

            # Append the BroadcastStep object to the list of substeps
            broadcast_substeps.append(broadcast_substep)

        self.substeps[StepType.BROADCAST].extend(broadcast_substeps)

    def generate_wireless_packet_reception_substeps(self, wireless_packet_reception, num_steps, broadcaster,
                                                    radius_constant, updated_node_data):
        reception_substeps = []

        # Get the node_object associated with the wireless packet reception using the to_id (t_id)
        node = next((node for node in updated_node_data if node.id == wireless_packet_reception.to_id), None)
        broadcaster_node = next((node for node in updated_node_data if node.id == broadcaster.from_id), None)

        if not node:
            # If the node is not found, return an empty list
            return

        # Calculate the time step for each substep
        time_step = (float(broadcaster.first_byte_transmission_time) - float(wireless_packet_reception.first_byte_received_time)) / (
                            num_steps - 1)

        # Generate the substeps
        for step in range(num_steps):
            # Calculate the time for the current substep
            substep_time = float(wireless_packet_reception.first_byte_received_time) + step * time_step
            radius = radius_constant * step
            # Create a WirelessReceptionStep object for the current substep
            reception_substep = WirelessPacketReceptionStep(
                time=substep_time, loc_x=node.loc_x,
                loc_y=node.loc_y, loc_z=node.loc_z,
                radius=radius, step_number=step,
                broadcast_loc_x=broadcaster_node.loc_x, broadcast_loc_y=broadcaster_node.loc_y,
                broadcast_loc_z=broadcaster_node.loc_z)

            # Append the WirelessReceptionStep object to the list of substeps
            reception_substeps.append(reception_substep)

        self.substeps[StepType.WIRELESS_PACKET_RECEPTION].extend(reception_substeps)

    def update_node_position(self, item):
        """
        Updates the position of a node_object in updated_node_data and adds a NodeUpdateStep to the substeps.

        Args:
        - item: an object representing the updated node_object position
        - updated_node_data: a dictionary containing updated node_object data

        Returns:
        - None
        """

        # Create a NodeUpdateStep object for this update
        node_update = NodeUpdateStep(time=float(item.time), node_id=item.id, red=item.r, green=item.g, blue=item.b,
                                     width=item.w, height=item.h,
                                     loc_x=item.x, loc_y=item.y, loc_z=item.z, description=item.descr)

        # Append the NodeUpdateStep object to the list of substeps
        self.substeps[StepType.NODE_UPDATE].append(node_update)
