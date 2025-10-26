from src.nodes.htmlnode import LeafNode
from src.nodes.textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    """
    Converts a text node to an HTML node of the given type.
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("invalid text node")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    desc: Takes a list of old_nodes, splits along a delimiter and returns a list of nodes after being split.
    inputs: List of text_nodes names old_nodes, a char delimiter, and a TextType.
    returns: list of split nodes
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            new_nodes.extend(split_node_delimiter(node, delimiter, text_type))
        else:
            new_nodes.append(node)

    return new_nodes
            
def split_node_delimiter(node, delimiter, text_type):
    """
    Splits a single node into multiple nodes along a delimiter
    """
    node_is_text = True

    new_nodes = []
    text_list = node.text.split(delimiter)

    if len(text_list) % 2 == 0:
        raise ValueError("unbalanced nodes")

    for i, text in enumerate(text_list):
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT if i % 2 == 0 else text_type))
    return new_nodes 
