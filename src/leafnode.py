from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag,value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.props is None:
            if self.tag is None:
                return self.value
            else:
                 return "<"+self.tag+">"+self.value+"</"+self.tag+">"
        elif self.tag is not None: 
            return "<"+self.tag+self.props_to_html()+">"+self.value+"</"+self.tag+">"



