import unittest

from enum import Enum
from textnode import TextNode, TextType
from utiliity import *


class TestSplit(unittest.TestCase):
    def test_split_no_delimiter(self):
        nodes = [TextNode("This is a text node")]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(result, nodes)

    def test_split_one_delimiter(self):
        nodes = [TextNode("This is _italic_ text")]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        expected = [
            TextNode("This is "),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text"),
        ]
        self.assertEqual(result, expected)

    def test_split_two_delimiters(self):
        nodes = [TextNode("This is _italic_ and _more italic_ text")]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        expected = [
            TextNode("This is "),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and "),
            TextNode("more italic", TextType.ITALIC),
            TextNode(" text"),
        ]
        self.assertEqual(result, expected)

    def test_split_unmatched_delimiter(self):
        nodes = [TextNode("This is _italic text")]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    def test_split_mixed_nodes(self):
        nodes = [
            TextNode("This is _italic_ text"),
            TextNode("This is a bold text", TextType.BOLD),
            TextNode("Another **bold** here"),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is _italic_ text"),
            TextNode("This is a bold text", TextType.BOLD),
            TextNode("Another "),
            TextNode("bold", TextType.BOLD),
            TextNode(" here"),
        ]
        self.assertEqual(result, expected)
        
    def test_split_mixed_node(self):
        nodes = [TextNode("This is `inline code`and a **bold** word and `more code`")]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("This is "),
            TextNode("inline code", TextType.CODE),
            TextNode("and a **bold** word and "),
            TextNode("more code", TextType.CODE),
        ]
        self.assertEqual(result, expected)
        
    def test_split_leading_trailing_delimiters(self):
        nodes = [TextNode("_Italic_ at start and _end_")]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        expected = [
            TextNode("Italic", TextType.ITALIC),
            TextNode(" at start and "),
            TextNode("end", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)


class TestText(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text")
        
    def test_italic_text(self):
        node = TextNode("This is an italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text")

    def test_code_text(self):
        node = TextNode("This is a code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text")

    def test_link_text(self):
        node = TextNode("This is a link text", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text")
        self.assertEqual(html_node.props["href"], "https://www.example.com")  # type: ignore

    def test_image_text(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://www.example.com/image.png")  # type: ignore
        self.assertEqual(html_node.props["alt"], "This is an image")  # type: ignore
        
    def test_unsupported_text_type(self):
        class FakeTextType(Enum):
            UNSUPPORTED = "unsupported"
        
        node = TextNode("This is unsupported", FakeTextType.UNSUPPORTED)  # type: ignore
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
            
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_images2(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://www.example.com)")
        self.assertListEqual([("link", "https://www.example.com")], matches)

    def test_extract_markdown_links2(self):
        matches = extract_markdown_links("This is text with a [link1](https://www.example1.com) and a [link2](https://www.example2.com)")
        self.assertListEqual([("link1", "https://www.example1.com"), ("link2", "https://www.example2.com")], matches)  

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_no_image(self):
        node = TextNode(
            "This is text with no images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no images", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.example2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.example2.com"
                ),
            ],
            new_nodes,
        )
        
    def test_split_no_link(self):
        node = TextNode(
            "This is text with no links",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links", TextType.TEXT),
            ],
            new_nodes,
        )  
        
    def test_text_to_textnodes(self):
        text = "This is a **bold** word, an _italic_ word, `inline code`, a [link](https://www.example.com), and an ![image](https://i.imgur.com/zjjcJKZ.png)."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word, an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word, ", TextType.TEXT),
            TextNode("inline code", TextType.CODE),
            TextNode(", a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
            TextNode(", and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)   