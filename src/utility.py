import re

from leafnode import LeafNode
from parentnode import ParentNode
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
    first_fence = next((i for i,l in enumerate(lines) if l.strip().startswith("```")), None)
    last_fence  = next((i for i in range(len(lines)-1, -1, -1) if lines[i].strip().startswith("```")), None)
    if first_fence is not None and last_fence is not None and last_fence > first_fence:
        return BlockType.CODE
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif first_line.startswith(">"):
        return BlockType.QUOTE
    elif re.match(r"^\d+\.\s", first_line):
        return BlockType.ORDERED_LIST
    elif re.match(r"^[-*+]\s", first_line):
        return BlockType.UNORDERED_LIST
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
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block.strip() == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    if not blocks:
        return ParentNode("div", [])
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                lines = [line.strip() for line in block.split("\n")]
                block = " ".join(lines)
                text_nodes = text_to_textnodes(block)
                children = [text_node_to_html_node(tn) for tn in text_nodes]
                html_nodes.append(ParentNode("p", children=children))
            case BlockType.HEADING:
                line = block.lstrip()
                level = len(line) - len(line.lstrip("#"))
                if level > 6:
                    level = 6
                content = line[level:].strip()
                text_nodes = text_to_textnodes(content)
                children = [text_node_to_html_node(tn) for tn in text_nodes]
                html_nodes.append(ParentNode(f"h{level}", children=children))
            case BlockType.ORDERED_LIST:
                norm = "\n".join(l.lstrip() for l in block.splitlines() if l.strip() != "")
                items = re.findall(r"^\d+\.\s+(.*?)(?=\n\d+\.|\Z)", norm, re.DOTALL | re.MULTILINE)

                list_items = []
                for item in items:
                    text = item.strip()
                    if not text:
                        continue
                    text_nodes = text_to_textnodes(text)
                    children = [text_node_to_html_node(tn) for tn in text_nodes]
                    list_items.append(ParentNode("li", children=children))

                if list_items:
                    html_nodes.append(ParentNode("ol", children=list_items))
            case BlockType.UNORDERED_LIST:
                norm = "\n".join(l.lstrip() for l in block.splitlines() if l.strip() != "")
                items = re.findall(r"^[-*+]\s+(.*?)(?=\n[-*+]\s|\Z)", norm, re.DOTALL | re.MULTILINE)
                list_items = []
                for item in items:
                    text_nodes = text_to_textnodes(item.strip())
                    children = [text_node_to_html_node(tn) for tn in text_nodes]
                    list_items.append(ParentNode("li", children=children))
                html_nodes.append(ParentNode("ul", children=list_items))
            case BlockType.CODE:
                raw = block.split("\n")
                inner = raw[1:-1]
                non_empty = [line for line in inner if line.strip() != ""]
                if non_empty:
                    min_indent = min(len(l) - len(l.lstrip(" ")) for l in non_empty)
                    inner = [l[min_indent:] if len(l) >= min_indent else "" for l in inner]
                code_content = "\n".join(inner)
                if not code_content.endswith("\n"):
                    code_content += "\n"
                code_text_node = TextNode(code_content, TextType.CODE)
                html_nodes.append(ParentNode("pre", children=[text_node_to_html_node(code_text_node)]))
            case BlockType.QUOTE:
                lines = []
                for ln in block.splitlines():
                    if ln.lstrip().startswith(">"):
                        # remove exactly one leading '>' and optional following space
                        s = ln.lstrip()[1:]
                        if s.startswith(" "):
                            s = s[1:]
                        lines.append(s.rstrip())
                quote_content = "<br>".join(lines)
                text_nodes = text_to_textnodes(quote_content)
                children = [text_node_to_html_node(tn) for tn in text_nodes]
                html_nodes.append(ParentNode("blockquote", children=children))
    return ParentNode("div", children=html_nodes)

