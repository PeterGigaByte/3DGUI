import xml.dom.minidom


class DOMXMLParser:
    def __init__(self):
        pass

    def parse_data(self, root):
        data = []
        elements = root.getElementsByTagName('record')  # Change 'record' to the appropriate tag name in your XML

        for element in elements:
            record = {}
            for child in element.childNodes:
                if child.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
                    record[child.tagName] = child.firstChild.nodeValue
            data.append(record)

        return data

    def parse(self, xml_file_path):
        dom_tree = xml.dom.minidom.parse(xml_file_path)
        root = dom_tree.documentElement
        return self.parse_data(root)

