class HTMLNode:
    def __init__(self,tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
                
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = "" 
        if self.props is not None:
            for i,v in self.props.items():
                result += " "+i+'="'+v+'"' 
        return result
    
    def __repr__(self):
        result = ""
        result += f"HTMLNode(tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props}"
        return result

