from network_elements.elements import Node, Nu
from utils.manage import get_objects_by_type


class AnimationApi:
    def __init__(self, renderer_api):
        self.renderer_api = renderer_api
        self.data = None

    def set_data(self, data):
        self.data = data

    def prepare_animation(self):
        nodes = get_objects_by_type(self.data.content, Node)
        for node in nodes:
            self.renderer_api.create_node(int(node.loc_x), int(node.loc_y), int(node.loc_z))
        self.renderer_api.renderer.GetRenderWindow().Render()


import xml.etree.ElementTree as ET

# Parse the XML data and extract the relevant attributes
xml_str = '''
<data>
    <p fId="1" fbTx="1" lbTx="1.000067199" tId="0" fbRx="1.002" lbRx="1.002067199"/>
    <p fId="2" fbTx="2" lbTx="2.000067199" tId="0" fbRx="2.002" lbRx="2.002067199"/>
    <p fId="3" fbTx="3" lbTx="3.000067199" tId="0" fbRx="3.002" lbRx="3.002067199"/>
</data>
'''

root = ET.fromstring(xml_str)

packet_data = []

for p in root.findall('p'):
    packet_data.append({
        'fId': p.get('fId'),
        'fb_tx': float(p.get('fbTx')),
        'lb_tx': float(p.get('lbTx')),
        'fb_rx': float(p.get('fbRx')),
        'lb_rx': float(p.get('lbRx')),
    })







