import unittest

from htmlnode import HTMLNode 



class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        print("\nCreating a HTMLNode only containing two value pair props and using the props_to_html method to unpack/print prpos\n")
        node = HTMLNode(props = {"href":"https://www.google.com", "target":"_blank",})
        print(node.props_to_html())

    def test_empty_HTMLNode(self):
        print("\nCreating and printing an empty HTMLNode\n")
        node = HTMLNode()
        print(node)

    def test_nochildren_HTMLNode(self):
        print("\nCreating and printing a HTMLNode with no children and no props\n")
        node = HTMLNode("h1", "This is a h1 header")
        print(node)

    def test_children_HTMLNode(self):
        print("\nCreating a HTMLNode with two children nodes and print the parent_node\n")
        node = HTMLNode("h1", "This is a h1 header")
        node2 = HTMLNode("p", "This is a paragraph")
        parent_node = HTMLNode(children = [node, node2])
        print(parent_node)

    def test_full_HTMLNOde(self):
        print("\nCreating a HTMLNode with all attributes set and printing\n")
        node = HTMLNode("h1", "This is a h1 header")
        node2 = HTMLNode("a", "This is a link (a) text", node, {"href":"https://www.google.com", "target":"_blank",})
        print(node2)

if __name__ == "__main__":
    unittest.main()
