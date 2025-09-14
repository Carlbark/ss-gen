from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag,value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.props == None:
            if self.tag == None:
                return self.value
            else:
                 return "<"+self.tag+">"+self.value+"</"+self.tag+">"
        else: 
            return "<"+self.tag+self.props_to_html()+">"+self.value+"</"+self.tag+">"



