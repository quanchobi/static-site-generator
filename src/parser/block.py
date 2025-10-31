from enum import Enum
import re

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

