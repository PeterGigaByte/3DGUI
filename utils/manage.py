def get_objects_by_type(objects, object_type):
    return [item for item in objects if isinstance(item, object_type)]


def get_node_coordinates_by_id(nodes, searched_node_id):
    for node in nodes:
        if node.id == searched_node_id:
            return int(node.loc_x), int(node.loc_y), int(node.loc_z)


def get_rendering_node_by_id(nodes, searched_node_id):
    for node in nodes:
        if node.node_id == searched_node_id:
            return node


def get_nonp2p_link_properties_by_node_id(nonp2p_link_properties_list, node_id):
    ip_address_list = []
    mac_list = []
    for nonp2p_link_properties in nonp2p_link_properties_list:
        if nonp2p_link_properties.id == node_id:
            ip, mac = nonp2p_link_properties.ip_address.split('~')
            ip_address_list.append(ip)
            mac_list.append(mac)
    return ip_address_list, mac_list


