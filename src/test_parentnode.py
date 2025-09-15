import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    
    def test_parent_to_html_with_a_child_and_props(self):
        child_node = LeafNode("a", "This is a link (a) text", {"href":"https://www.google.com"})
        parent_node = ParentNode("div", [child_node], {"target":"_blank"})
        self.assertEqual(parent_node.to_html(), '<div target="_blank"><a href="https://www.google.com">This is a link (a) text</a></div>')
            
    def test_parent_to_html_with_a_child(self):
        child_node = LeafNode("a", "This is a link (a) text", {"href":"https://www.google.com"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><a href="https://www.google.com">This is a link (a) text</a></div>')
            
    def test_parent_to_html_with_raw_child(self):
        child_node = LeafNode(None, "raw text")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div>raw text</div>')

    def test_to_html_with_one_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_two_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("b", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><b>child2</b></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_to_html_notag(self):
        node = ParentNode(None,None)
        with self.assertRaises(ValueError):
            node.to_html()
            
    def test_parent_to_html_nochild(self):
        node = ParentNode("a",None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_nochild2(self):
        node = ParentNode("a",[])
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
