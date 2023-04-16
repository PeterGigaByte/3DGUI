from network_elements.tags import IpTags


class Ip:
    def __init__(self, n, addresses):
        self.n = n
        self.addresses = addresses

    def to_dict(self):
        return {
            IpTags.N_TAG.value: self.n
        }

