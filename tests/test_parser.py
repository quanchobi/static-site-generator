import unittest

from src.nodes.textnode import TextType, TextNode
from src.nodes.htmlnode import HTMLNode, LeafNode, ParentNode

from src.parser import split_nodes_delimiter
from src.parser import extract_markdown_images
from src.parser import extract_markdown_links

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_italics(self):
        node = TextNode("This is text with an *italics* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, 
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italics", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_italic_at_begin(self):
        node = TextNode("*This* is text with an italics word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, 
            [
                TextNode("This", TextType.ITALIC),
                TextNode(" is text with an italics word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_italic_unbalanced_nodes(self):
        with self.assertRaises(ValueError):
            node = TextNode("*This* is text with an odd number of *delimiters", TextType.TEXT)
            split_nodes_delimiter([node], "*", TextType.ITALIC)

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

