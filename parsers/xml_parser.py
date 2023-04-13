import xml.etree.ElementTree as ET


class XMLParser:
    def parse(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
