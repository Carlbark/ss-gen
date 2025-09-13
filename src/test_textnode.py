import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq1(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is some anchor text", TextType.LINK,"https://www.boot.dev")
        node2 = TextNode("This is some anchor text", TextType.LINK,"https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_noteq1(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node,node2)

    def test_noteq2(self):
        node = TextNode("This is a test node", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        self.assertNotEqual(node,node2)

    def test_noteq3(self):
        node = TextNode("This is some anchor text", TextType.LINK,"https://www.boot.dev")
        node2 = TextNode("This is some anchor text", TextType.LINK,"https://www.boot.org")
        self.assertNotEqual(node,node2)

if __name__ == "__main__":
    unittest.main()
