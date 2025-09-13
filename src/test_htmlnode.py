import unittest

from htmlnode import HTMLNode 



class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props = {"href":"https://www.google.com", "target":"_blank",})
        print(node.props_to_html())

    def test_empty_HTMLNode(self):
        node = HTMLNode()
        print(node)

    def test_nochildren_HTMLNode(self):
        node = HTMLNode("h1", "This is a h1 header")
        print(node)

    def test_children_HTMLNode(self):
        node = HTMLNode("h1", "This is a h1 header")
        node2 = HTMLNode("p", "This is a paragraph")
        parent_node = HTMLNode(children = [node, node2])
        print(parent_node)

    def test_full_HTMLNOde(self):
        node = HTMLNode("h1", "This is a h1 header")
        node2 = HTMLNode("a", "This is a link (a) text", node, {"href":"https://www.google.com", "target":"_blank",})
        print(node2)

if __name__ == "__main__":
    unittest.main()
