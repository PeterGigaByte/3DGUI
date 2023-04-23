from xml.dom.minidom import parse
from network_elements.elements import (
    Address, Anim, Ip, IpV6, Link, Ncs, Node, NonP2pLinkProperties,
    NodeUpdate, WiredPacket, Broadcaster, Resource, WirelessPacketReception
)
from network_elements.tags import NetworkElementTags, AnimTags, NodeTags, NuTags, NonP2pLinkPropertiesTags, AddressTags, \
    IpTags, IpV6Tags, NcsTags, PTags, WprTags, PrTags, ResTags, LinkTags


class DOMXMLParser:
    @staticmethod
    def get_attribute_with_none(node, attribute_name):
        attr_value = node.getAttribute(attribute_name)
        return None if attr_value == "" else attr_value

    def __init__(self):
        pass

    def parse(self, xml_file_path):
        root = parse(xml_file_path)

        # anim tag
        anim = dom_parse_anim(root)
        anim_content = []
        anim_content.extend(dom_parse_node(root))
        anim_content.extend(dom_parse_nu(root))
        anim_content.extend(dom_parse_non_link_properties(root))
        anim_content.extend(dom_parse_ip(root))
        anim_content.extend(dom_parse_ipv(root))
        anim_content.extend(dom_parse_p(root))
        anim_content.extend(dom_parse_wpr(root))
        anim_content.extend(dom_parse_pr(root))
        anim_content.extend(dom_parse_res(root))
        anim_content.extend(dom_parse_link(root))
        anim_content.extend(dom_parse_nsc(root))
        anim.content = anim_content
        return anim


def dom_parse_anim(data):
    anim_node = data.childNodes[0]
    return Anim(DOMXMLParser.get_attribute_with_none(anim_node, AnimTags.VER_TAG),
                DOMXMLParser.get_attribute_with_none(anim_node, AnimTags.FILE_TYPE_TAG)
                )


def dom_parse_node(data):
    nodes = data.getElementsByTagName(NetworkElementTags.NODE_TAG.value)
    data_list = []
    for node in nodes:
        data_list.append(Node(DOMXMLParser.get_attribute_with_none(node, NodeTags.ID_TAG),
                              DOMXMLParser.get_attribute_with_none(node, NodeTags.SYS_ID_TAG),
                              DOMXMLParser.get_attribute_with_none(node, NodeTags.LOC_X_TAG),
                              DOMXMLParser.get_attribute_with_none(node, NodeTags.LOC_Y_TAG),
                              DOMXMLParser.get_attribute_with_none(node, NodeTags.LOC_Z_TAG)
                              ))
    return data_list


def dom_parse_nu(data):
    nus = data.getElementsByTagName(NetworkElementTags.NU_TAG.value)
    data_list = []
    for nu in nus:
        data_list.append(NodeUpdate(DOMXMLParser.get_attribute_with_none(nu, NuTags.P_TAG),
                                    DOMXMLParser.get_attribute_with_none(nu, NuTags.T_TAG),
                                    DOMXMLParser.get_attribute_with_none(nu, NuTags.ID_TAG),
                                    DOMXMLParser.get_attribute_with_none(nu, NuTags.COLOR_R_TAG),
                                    DOMXMLParser.get_attribute_with_none(nu, NuTags.COLOR_G_TAG),
                                    DOMXMLParser.get_attribute_with_none(nu, NuTags.COLOR_B_TAG),
                                    DOMXMLParser.get_attribute_with_none(nu, NuTags.WIDTH_TAG),
                                    DOMXMLParser.get_attribute_with_none(nu, NuTags.HEIGHT_TAG),
                                    DOMXMLParser.get_attribute_with_none(nu, NuTags.COORD_X_TAG),
                                    DOMXMLParser.get_attribute_with_none(nu, NuTags.COORD_Y_TAG),
                                    DOMXMLParser.get_attribute_with_none(nu, NuTags.COORD_Z_TAG),
                                    DOMXMLParser.get_attribute_with_none(nu, NuTags.DESCRIPTION_TAG),
                                    ))
    return data_list


def dom_parse_non_link_properties(data):
    non_link_properties_list = data.getElementsByTagName(NetworkElementTags.NONP2PLINKPROPERTIES_TAG.value)
    data_list = []
    for non_link_property in non_link_properties_list:
        data_list.append(NonP2pLinkProperties(
            DOMXMLParser.get_attribute_with_none(non_link_property, NonP2pLinkPropertiesTags.ID_TAG),
            DOMXMLParser.get_attribute_with_none(non_link_property, NonP2pLinkPropertiesTags.IP_ADDRESS_TAG),
            DOMXMLParser.get_attribute_with_none(non_link_property, NonP2pLinkPropertiesTags.CHANNEL_TYPE_TAG)
            ))
    return data_list


def dom_parse_ip(data):
    ip_list = data.getElementsByTagName(NetworkElementTags.IP_TAG.value)
    data_list = []
    for ip in ip_list:
        data_list.append(Ip(DOMXMLParser.get_attribute_with_none(ip, IpTags.N_TAG),
                            dom_parse_address(ip)
                            ))
    return data_list


def dom_parse_ipv(data):
    ipv_list = data.getElementsByTagName(NetworkElementTags.IPV6_TAG.value)
    data_list = []
    for ipv in ipv_list:
        data_list.append(IpV6(DOMXMLParser.get_attribute_with_none(ipv, IpV6Tags.N_TAG),
                              dom_parse_address(ipv)
                              ))
    return data_list


def dom_parse_address(data):
    address_list = data.getElementsByTagName(NetworkElementTags.ADDRESS_TAG.value)
    data_list = []
    for address in address_list:
        data_list.append(Address(address.childNodes[0].nodeValue,
                                 ))
    return data_list


def dom_parse_nsc(data):
    nsc_list = data.getElementsByTagName(NetworkElementTags.NCS_TAG.value)
    data_list = []
    for nsc in nsc_list:
        data_list.append(Ncs(DOMXMLParser.get_attribute_with_none(nsc, NcsTags.NC_ID_TAG),
                             DOMXMLParser.get_attribute_with_none(nsc, NcsTags.N_TAG),
                             DOMXMLParser.get_attribute_with_none(nsc, NcsTags.T_TAG)
                             ))
    return data_list


def dom_parse_p(data):
    p_list = data.getElementsByTagName(NetworkElementTags.P_TAG.value)
    data_list = []
    for p in p_list:
        data_list.append(WiredPacket(DOMXMLParser.get_attribute_with_none(p, PTags.FROM_ID_TAG),
                                     DOMXMLParser.get_attribute_with_none(p, PTags.FB_TX_TAG),
                                     DOMXMLParser.get_attribute_with_none(p, PTags.LB_TX_TAG),
                                     DOMXMLParser.get_attribute_with_none(p, PTags.META_INFO_TAG),
                                     DOMXMLParser.get_attribute_with_none(p, PTags.TO_ID_TAG),
                                     DOMXMLParser.get_attribute_with_none(p, PTags.FB_RX_TAG),
                                     DOMXMLParser.get_attribute_with_none(p, PTags.LB_RX_TAG)
                                     ))
    return data_list


def dom_parse_wpr(data):
    wpr_list = data.getElementsByTagName(NetworkElementTags.WPR_TAG.value)
    data_list = []
    for wpr in wpr_list:
        data_list.append(WirelessPacketReception(DOMXMLParser.get_attribute_with_none(wpr, WprTags.U_ID_TAG),
                                                 DOMXMLParser.get_attribute_with_none(wpr, WprTags.T_ID_TAG),
                                                 DOMXMLParser.get_attribute_with_none(wpr, WprTags.FB_RX_TAG),
                                                 DOMXMLParser.get_attribute_with_none(wpr, WprTags.LB_RX_TAG)
                                                 ))
    return data_list


def dom_parse_pr(data):
    pr_list = data.getElementsByTagName(NetworkElementTags.PR_TAG.value)
    data_list = []
    for pr in pr_list:
        data_list.append(Broadcaster(DOMXMLParser.get_attribute_with_none(pr, PrTags.U_ID_TAG),
                                     DOMXMLParser.get_attribute_with_none(pr, PrTags.F_ID_TAG),
                                     DOMXMLParser.get_attribute_with_none(pr, PrTags.FB_TX_TAG),
                                     DOMXMLParser.get_attribute_with_none(pr, PrTags.META_INFO_TAG)
                                     ))
    return data_list


def dom_parse_res(data):
    res_list = data.getElementsByTagName(NetworkElementTags.RES_TAG.value)
    data_list = []
    for res in res_list:
        data_list.append(Resource(DOMXMLParser.get_attribute_with_none(res, ResTags.RID_TAG),
                                  DOMXMLParser.get_attribute_with_none(res, ResTags.P_TAG)
                                  ))
    return data_list


def dom_parse_link(data):
    link_list = data.getElementsByTagName(NetworkElementTags.LINK_TAG.value)
    data_list = []
    for link in link_list:
        data_list.append(Link(DOMXMLParser.get_attribute_with_none(link, LinkTags.FROM_ID_TAG),
                              DOMXMLParser.get_attribute_with_none(link, LinkTags.TO_ID_TAG),
                              DOMXMLParser.get_attribute_with_none(link, LinkTags.FD_TAG),
                              DOMXMLParser.get_attribute_with_none(link, LinkTags.TD_TAG),
                              DOMXMLParser.get_attribute_with_none(link, LinkTags.LD_TAG)
                              ))
    return data_list
