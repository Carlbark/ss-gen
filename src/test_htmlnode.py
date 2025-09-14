import unittest

from htmlnode import HTMLNode 



class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props = {"href":"https://www.google.com", "target":"_blank",})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_empty_HTMLNode(self):
        node = HTMLNode()
        # Test that the node was created with default values
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props) 

    def test_nochildren_HTMLNode(self):
        node = HTMLNode("h1", "This is a h1 header")
        # Test that the node has the expected tag and value
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "This is a h1 header")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    def test_children_HTMLNode(self):
        node = HTMLNode("h1", "This is a h1 header")
        node2 = HTMLNode("p", "This is a paragraph")
        parent_node = HTMLNode(children=[node, node2])
    
        # Test that the parent has the expected children
        self.assertEqual(len(parent_node.children), 2)
        self.assertEqual(parent_node.children[0].tag, "h1")
        self.assertEqual(parent_node.children[1].tag, "p")

    def test_full_HTMLNode(self):
        # Note: Fixed typo "HTMLNOde" -> "HTMLNode"
        node = HTMLNode("h1", "This is a h1 header")
        node2 = HTMLNode("a", "This is a link (a) text", [node], {"href": "https://www.google.com", "target": "_blank"})
    
        # Test all the attributes
        self.assertEqual(node2.tag, "a")
        self.assertEqual(node2.value, "This is a link (a) text")
        self.assertEqual(len(node2.children), 1)
        self.assertEqual(node2.props["href"], "https://www.google.com")
        self.assertEqual(node2.props["target"], "_blank")

if __name__ == "__main__":
    unittest.main()
