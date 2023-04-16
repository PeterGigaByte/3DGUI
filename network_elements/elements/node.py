from network_elements.tags import NodeTags


class Node:
    def __init__(self, id, sys_id, loc_x, loc_y, loc_z):
        self.id = id
        self.sys_id = sys_id
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.loc_z = loc_z

    def to_dict(self):
        return {
            NodeTags.ID_TAG.value: self.id,
            NodeTags.SYS_ID_TAG.value: self.sys_id,
            NodeTags.LOC_X_TAG.value: self.loc_x,
            NodeTags.LOC_Z_TAG.value: self.loc_z
        }