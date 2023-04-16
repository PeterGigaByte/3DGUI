from network_elements.tags import WprTags


class Wpr:
    def __init__(self, u_id, t_id, fb_rx, lb_rx):
        self.u_id = u_id
        self.t_id = t_id
        self.fb_rx = fb_rx
        self.lb_rx = lb_rx

    def to_dict(self):
        return {
            WprTags.U_ID_TAG.value: self.u_id,
            WprTags.T_ID_TAG.value: self.t_id,
            WprTags.FB_RX_TAG.value: self.fb_rx,
            WprTags.LB_RX_TAG.value: self.lb_rx
        }