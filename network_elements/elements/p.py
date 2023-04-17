from network_elements.tags import PTags


class P:
    def __init__(self, f_id, fb_tx, lb_tx, meta_info, t_id, fb_rx, lb_rx):
        self.f_id = f_id
        self.fb_tx = fb_tx
        self.lb_tx = lb_tx
        self.meta_info = meta_info
        self.t_id = t_id
        self.fb_rx = fb_rx
        self.lb_rx = lb_rx

    def to_dict(self):
        return {
            PTags.FROM_ID_TAG.value: self.f_id,
            PTags.FB_TX_TAG.value: self.fb_tx,
            PTags.LB_TX_TAG.value: self.lb_tx,
            PTags.META_INFO_TAG.value: self.meta_info,
            PTags.TO_ID_TAG.value: self.t_id,
            PTags.FB_RX_TAG.value: self.fb_rx,
            PTags.LB_RX_TAG.value: self.lb_rx
        }