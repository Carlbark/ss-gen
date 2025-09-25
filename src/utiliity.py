import re

from leafnode import LeafNode
from textnode import TextNode, TextType
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    ORDERED_LIST = "ol"
    UNORDERED_LIST = "ul"
    CODE = "c"
    QUOTE = "q"

def block_to_block_type(block):
    lines = block.split("\n")
    first_line = lines[0].strip()
    if first_line.startswith("#"):
        return BlockType.HEADING
    elif first_line.startswith(">"):
        return BlockType.QUOTE
    elif re.match(r"^\d+\.\s", first_line):
        return BlockType.ORDERED_LIST
    elif re.match(r"^[-*+]\s", first_line):
        return BlockType.UNORDERED_LIST
    elif first_line.startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH

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

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    images = []
    for alt, url in matches:
        images.append((alt, url))
    return images

def extract_markdown_links(text):
    matches = re.findall(r"(?<!\!)\[([^\]]+)\]\(([^)]+)\)", text)
    links = [(alt, url) for alt, url in matches]
    return links

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text = node.text
            images = extract_markdown_images(text)
            for alt, url in images:
                parts = text.split(f"![{alt}]({url})", 1)
                if parts[0]:
                    result.append(TextNode(parts[0]))
                result.append(TextNode(alt, TextType.IMAGE, url))
                text = parts[1] if len(parts) > 1 else ""
            if text:
                result.append(TextNode(text))
        else:
            result.append(node)
    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text = node.text
            links = extract_markdown_links(text)
            if len(links) == 0:
                result.append(node)
                continue
            for alt, url in links:
                parts = text.split(f"[{alt}]({url})", 1)
                if parts[0]:
                    result.append(TextNode(parts[0]))
                result.append(TextNode(alt, TextType.LINK, url))
                text = parts[1] if len(parts) > 1 else ""
            if text:
                result.append(TextNode(text))
        else:
            result.append(node)
    return result

def text_to_textnodes(text):
    nodes = [TextNode(text)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes

def markdown_to_blocks(markdown):
    paragraphs = markdown.split("\n\n")
    blocks = []
    for paragraph in paragraphs:
        if paragraph.strip():
            blocks.append(paragraph.strip())
    return blocks
