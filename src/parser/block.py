from enum import Enum
import re

from parser.inline import text_to_textnodes, text_node_to_html_node
from nodes.htmlnode import ParentNode
from nodes.textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"

def markdown_to_blocks(markdown):
    """
    Takes a raw markdown string and returns a list of blocks
    """
    blocks = markdown.split("\n\n")

    return list(filter(None, (b.strip() for b in blocks)))

def block_to_block_type(block):
    """
    Takes a single block of markdown text and returns the BlockType representing the type of block it is.
    """
    if re.match("^#{1,6} .+", block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    # extra paranoia strips
    if all(line.strip().startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.strip().startswith("- ") for line in lines):
        return BlockType.UL

    if all(line.strip().startswith(f"{i+1}. ") for i, line in enumerate(lines)):
        return BlockType.OL

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                nodes.append(paragraph_to_html_node(block))
            case BlockType.HEADING:
                nodes.append(heading_to_html_node(block))
            case BlockType.CODE:
                nodes.append(code_to_html_node(block))
            case BlockType.QUOTE:
                nodes.append(quote_to_html_node(block))
            case BlockType.UL:
                nodes.append(ul_to_html_node(block))
            case BlockType.OL:
                nodes.append(ol_to_html_node(block))

    return ParentNode("div", nodes)

def text_to_children(text):
    """
    Returns a list of inline elements found in a markdown text block
    """
    textnodes = text_to_textnodes(text)
    return [text_node_to_html_node(textnode) for textnode in textnodes]

def paragraph_to_html_node(block):
    """
    Takes a block of text representing the contents of a markdown paragraph block.
    Takes the markdown paragraph block, makes it a single line separarted by spaces, and creates a ParentNode based on the contents and children.
    Returns a ParentNode
    """
    lines = [line.strip() for line in block.split("\n")]
    content = " ".join(lines) # replace newlines with spaces
    children = text_to_children(content)
    return ParentNode("p", children)

def heading_to_html_node(block):
    # count number of hashtags in the header
    i = 0
    for c in block:
        if c != "#":
            break
        i += 1

    if i == 0:
        raise ValueError("Invalid header block")

    block = block.strip("#").strip()
    children = text_to_children(block)
    return ParentNode(f"h{i}", children)

def code_to_html_node(block):
    """
    Takes a block of text representing the contents of a markdown code block.
    """
    if not (block.startswith("```") and block.endswith("```")):
        raise ValueError("Invalid code block")
    content = block.strip("```").lstrip("\n").strip(" ")
    # might need to do extra string cleaning
    code_text_node = TextNode(content, TextType.TEXT)
    code_html_node = text_node_to_html_node(code_text_node)

    return ParentNode("pre", [ParentNode("code", [code_html_node])])

def quote_to_html_node(block):
    lines = block.split("\n")
    if not all(line.startswith(">") for line in lines):
        raise ValueError("Invalid quote block")

    lines = [line.lstrip(">").strip() for line in lines]
    code_block_content = " ".join(lines)

    children = text_to_children(code_block_content)

    return ParentNode("blockquote", children)

def ul_to_html_node(block):
# for a ul, each line must start with "-". Split into lines, then strip("-") this then strip the whitespace
    lines = block.split("\n")
    if not all(line.startswith("-") for line in lines):
        raise ValueError("Invalid unordered list")

    lines = [line.lstrip("-").strip() for line in lines]
    # each line must be turned into nodes with the tag li
    # find children of the line (ie for nested lists)
    line_nodes = []
    for line in lines:
        line_node_children = text_to_children(line)
        line_nodes.append(ParentNode("li", line_node_children))
    return ParentNode("ul", line_nodes)

def ol_to_html_node(block):
    lines = block.split("\n")
    if not all(line[0].isnumeric() for line in lines):
        raise ValueError("Invalid ordered list")

    # remove number and whitespace from entries
    lines = [line.lstrip(f"{i+1}.").strip() for i, line in enumerate(lines)]

    line_nodes = []
    for line in lines:
        line_node_children = text_to_children(line)
        line_nodes.append(ParentNode("li", line_node_children))

    return ParentNode("ol", line_nodes)
    
