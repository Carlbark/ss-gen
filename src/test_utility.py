import unittest

from enum import Enum
from textnode import TextNode, TextType
from utility import *
from leafnode import LeafNode
from parentnode import ParentNode
from htmlnode import HTMLNode

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
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("This is a normal paragraph\nwith two lines"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("# This is a header"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## This is a level 2 header"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### This is a level 3 header"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("- This is a list item\n- This is another list item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("* This is a list item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. This is a numbered list item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("This is a normal paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("> This is a blockquote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("```\nThis is a code block\n```"), BlockType.CODE)
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html() 
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
This is text that _should_ remain
the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_unorderded_list(self):
        md = """
- This is a list item with **bold** text
- This is another item with `code`
- Final item with a [link](https://www.example.com)

    Code in the middle
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list item with <b>bold</b> text</li><li>This is another item with <code>code</code></li><li>Final item with a <a href=\"https://www.example.com\">link</a></li></ul><p>Code in the middle</p></div>",
        )  
        
    def test_ordered_list(self):
        md = """
1. This is a list item with **bold** text
2. This is another item with `code`
3. Final item with a [link](https://www.example.com)
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is a list item with <b>bold</b> text</li><li>This is another item with <code>code</code></li><li>Final item with a <a href=\"https://www.example.com\">link</a></li></ol></div>",
        )
        
    def test_blockquote(self):
        md = """
> This is a blockquote
> with multiple lines
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote<br>with multiple lines</blockquote></div>",
        )
        
    def test_heading(self):
        md = """
# This is a level 1 heading

## This is a level 2 heading

### This is a level 3 heading
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a level 1 heading</h1><h2>This is a level 2 heading</h2><h3>This is a level 3 heading</h3></div>",
        )
        
    def test_text_mixed(self):
        md = """
Some **bold** text, some _italic_ text, and some `inline code`.

```
def hello_world():
    print("Hello, world!")
```

> This is a blockquote with a [link](https://www.example.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)

- List item 1 with **bold** text
- List item 2 with `code`
"""
        self.maxDiff = None
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Some <b>bold</b> text, some <i>italic</i> text, and some <code>inline code</code>.</p><pre><code>def hello_world():\n    print(\"Hello, world!\")\n</code></pre><blockquote>This is a blockquote with a <a href=\"https://www.example.com\">link</a> and an <img src=\"https://i.imgur.com/zjjcJKZ.png\" alt=\"image\"></img></blockquote><ul><li>List item 1 with <b>bold</b> text</li><li>List item 2 with <code>code</code></li></ul></div>",
        )