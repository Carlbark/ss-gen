from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have tags")
        if self.children is None or self.children == []:
            raise ValueError("All parent nodes must have children")
        if self.props == None:
            result = "<"+self.tag+">"
        else:
            result = "<"+self.tag+self.props_to_html()+">"
        for child in self.children:
            result += child.to_html()
        result += "</"+self.tag+">"
        return result


