def get_objects_by_type(objects, object_type):
    return [item for item in objects if isinstance(item, object_type)]


def get_node_coor_by_id(nodes, searched_node):
    for node in nodes:
        if node.id == searched_node:
            return int(node.loc_x), int(node.loc_y), int(node.loc_z)
