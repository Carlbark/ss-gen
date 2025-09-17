

from leafnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(None, text_node.text)
            case TextType.ITALIC | TextType.BOLD | TextType.CODE:
                tag = text_node.text_type.value
                return LeafNode(tag, text_node.text)
            case TextType.LINK:
                return LeafNode("a", text_node.text, {"href": text_node.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            case _:
                raise ValueError(f"Unsupported text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            new_nodes = node.text.split(delimiter)
            if len(new_nodes) % 2 == 0:
                raise ValueError(f"Unmatched delimiter: {delimiter}")
            for i, new_node in enumerate(new_nodes):
                if i % 2 == 0:
                    if new_node:
                        result.append(TextNode(new_node))
                else:
                    result.append(TextNode(new_node, text_type))
        else:
            result.append(node)
    return result