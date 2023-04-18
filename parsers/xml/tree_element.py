from xml.etree import ElementTree

from network_elements.elements import (
    Address, Anim, Ip, IpV6, Link, Ncs, Node, NonP2pLinkProperties,
    NodeUpdate, WiredPacket, Broadcaster, Resource, WirelessPacketReception
)
from network_elements.tags import NetworkElementTags, AnimTags, NodeTags, NuTags, NonP2pLinkPropertiesTags, AddressTags, \
    IpTags, IpV6Tags, NcsTags, PTags, WprTags, PrTags, ResTags, LinkTags


def parse_tag(selected_tag):
    match selected_tag.tag:
        case NetworkElementTags.ANIM_TAG.value:
            return Anim(selected_tag.attrib.get(AnimTags.VER_TAG),
                        selected_tag.attrib.get(AnimTags.FILE_TYPE_TAG)
                        )

        case NetworkElementTags.NODE_TAG.value:
            return Node(selected_tag.attrib.get(NodeTags.ID_TAG),
                        selected_tag.attrib.get(NodeTags.SYS_ID_TAG),
                        selected_tag.attrib.get(NodeTags.LOC_X_TAG),
                        selected_tag.attrib.get(NodeTags.LOC_Y_TAG),
                        selected_tag.attrib.get(NodeTags.LOC_Z_TAG)
                        )

        case NetworkElementTags.NU_TAG.value:
            return NodeUpdate(selected_tag.attrib.get(NuTags.P_TAG),
                              selected_tag.attrib.get(NuTags.T_TAG),
                              selected_tag.attrib.get(NuTags.ID_TAG),
                              selected_tag.attrib.get(NuTags.COLOR_R_TAG),
                              selected_tag.attrib.get(NuTags.COLOR_G_TAG),
                              selected_tag.attrib.get(NuTags.COLOR_B_TAG),
                              selected_tag.attrib.get(NuTags.WIDTH_TAG),
                              selected_tag.attrib.get(NuTags.HEIGHT_TAG),
                              selected_tag.attrib.get(NuTags.COORD_X_TAG),
                              selected_tag.attrib.get(NuTags.COORD_Y_TAG),
                              selected_tag.attrib.get(NuTags.COORD_Z_TAG),
                              selected_tag.attrib.get(NuTags.DESCRIPTION_TAG),
                              )

        case NetworkElementTags.NONP2PLINKPROPERTIES_TAG.value:
            return NonP2pLinkProperties(selected_tag.attrib.get(NonP2pLinkPropertiesTags.ID_TAG),
                                        selected_tag.attrib.get(NonP2pLinkPropertiesTags.IP_ADDRESS_TAG),
                                        selected_tag.attrib.get(NonP2pLinkPropertiesTags.CHANNEL_TYPE_TAG)
                                        )
        case NetworkElementTags.IP_TAG.value:
            addresses = selected_tag.findall(NetworkElementTags.ADDRESS_TAG.value)
            addresses_list = []
            for _ in addresses:
                addresses_list.append(Address(selected_tag.attrib.get(AddressTags.IP_ADDRESS_TAG)))
            return Ip(selected_tag.attrib.get(IpTags.N_TAG), addresses_list)

        case NetworkElementTags.IPV6_TAG.value:
            addresses = selected_tag.findall(NetworkElementTags.ADDRESS_TAG.value)
            addresses_list = []
            for _ in addresses:
                addresses_list.append(Address(selected_tag.attrib.get(AddressTags.IP_ADDRESS_TAG)))
            return IpV6(selected_tag.attrib.get(IpV6Tags.N_TAG), addresses_list)

        case NetworkElementTags.ADDRESS_TAG.value:
            return Address(selected_tag.attrib.get(AddressTags.IP_ADDRESS_TAG))

        case NetworkElementTags.NCS_TAG.value:
            return Ncs(selected_tag.attrib.get(NcsTags.NC_ID_TAG),
                       selected_tag.attrib.get(NcsTags.N_TAG),
                       selected_tag.attrib.get(NcsTags.T_TAG)
                       )

        case NetworkElementTags.P_TAG.value:
            return WiredPacket(selected_tag.attrib.get(PTags.FROM_ID_TAG),
                               selected_tag.attrib.get(PTags.FB_TX_TAG),
                               selected_tag.attrib.get(PTags.LB_TX_TAG),
                               selected_tag.attrib.get(PTags.META_INFO_TAG),
                               selected_tag.attrib.get(PTags.TO_ID_TAG),
                               selected_tag.attrib.get(PTags.FB_RX_TAG),
                               selected_tag.attrib.get(PTags.LB_RX_TAG)
                               )

        case NetworkElementTags.WPR_TAG.value:
            return WirelessPacketReception(selected_tag.attrib.get(WprTags.U_ID_TAG),
                                           selected_tag.attrib.get(WprTags.T_ID_TAG),
                                           selected_tag.attrib.get(WprTags.FB_RX_TAG),
                                           selected_tag.attrib.get(WprTags.LB_RX_TAG)
                                           )
        case NetworkElementTags.PR_TAG.value:
            return Broadcaster(selected_tag.attrib.get(PrTags.U_ID_TAG),
                               selected_tag.attrib.get(PrTags.F_ID_TAG),
                               selected_tag.attrib.get(PrTags.FB_TX_TAG),
                               selected_tag.attrib.get(PrTags.META_INFO_TAG)
                               )
        case NetworkElementTags.RES_TAG.value:
            return Resource(selected_tag.attrib.get(ResTags.RID_TAG),
                            selected_tag.attrib.get(ResTags.P_TAG)
                            )
        case NetworkElementTags.LINK_TAG.value:
            return Link(selected_tag.attrib.get(LinkTags.FROM_ID_TAG),
                        selected_tag.attrib.get(LinkTags.TO_ID_TAG),
                        selected_tag.attrib.get(LinkTags.FD_TAG),
                        selected_tag.attrib.get(LinkTags.TD_TAG),
                        selected_tag.attrib.get(LinkTags.LD_TAG)
                        )


class ElementTreeXMLParser:
    def __init__(self, bottom_dock_widget):
        self.bottom_dock_widget = bottom_dock_widget
        self.anim = None
        self.none_type = None
        pass

    def parse(self, xml_file_path):
        self.bottom_dock_widget.log('Xml parser begin')
        self.bottom_dock_widget.log('File path: {0}'.format(xml_file_path))
        tree = ElementTree.parse(xml_file_path)
        tags = tree.getroot()

        # anim tag
        self.anim = parse_tag(tags)
        anim_content = []

        # none_type counter
        self.none_type = 0

        # read all tags
        for selected_tag in tags:
            item = parse_tag(selected_tag)

            # check if some item has no type - test functionality
            if item is None:
                self.none_type += 1
                print(f'Unknown tag in main content : {item}')
            anim_content.append(parse_tag(selected_tag))

        # add to anim object as content
        self.anim.content = anim_content

        # info print
        self.bottom_dock_widget.log(f'NoneType tags : {self.none_type}')
        self.bottom_dock_widget.log('Xml parser end')

        return self.anim

