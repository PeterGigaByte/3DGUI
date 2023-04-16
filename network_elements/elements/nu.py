from network_elements.tags import NuTags


class Nu:
    def __init__(self, p, t, id, r, g, b, w, h, x, y, descr):
        self.p = p
        self.t = t
        self.id = id
        self.r = r
        self.g = g
        self.b = b
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.descr = descr

    def to_dict(self):
        return {
            NuTags.P_TAG.value: self.p,
            NuTags.T_TAG.value: self.t,
            NuTags.ID_TAG.value: self.id,
            NuTags.COLOR_R_TAG.value: self.r,
            NuTags.COLOR_G_TAG.value: self.g,
            NuTags.COLOR_B_TAG.value: self.b,
            NuTags.WIDTH_TAG.value: self.w,
            NuTags.HEIGHT_TAG.value: self.h,
            NuTags.COORD_X_TAG.value: self.x,
            NuTags.COORD_Y_TAG.value: self.y,
            NuTags.DESCRIPTION_TAG.value: self.descr
        }