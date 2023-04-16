from network_elements.tags import PrTags


class Pr:
    def __init__(self, u_id, f_id, fb_tx, meta_info):
        self.u_id = u_id
        self.f_id = f_id
        self.fb_tx = fb_tx
        self.meta_info = meta_info

    def to_dict(self):
        return {
            PrTags.U_ID_TAG.value: self.u_id,
            PrTags.F_ID_TAG.value: self.f_id,
            PrTags.FB_TX_TAG.value: self.fb_tx,
            PrTags.META_INFO_TAG.value: self.meta_info
        }
