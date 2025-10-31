import unittest

from src.nodes.textnode import TextType, TextNode
from src.nodes.htmlnode import HTMLNode, LeafNode, ParentNode
from src.parser.block import BlockType

from src.parser.inline import split_nodes_delimiter
from src.parser.inline import extract_markdown_images, extract_markdown_links
from src.parser.inline import split_nodes_link, split_nodes_image
from src.parser.inline import text_to_textnodes

from src.parser.block import markdown_to_blocks, block_to_block_type

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

    def test_extract_markdown_images_no_image(self):
        matches = extract_markdown_images(
            "This text has no image"
        )
        self.assertEqual(matches, [])

    def test_extract_markdown_links_no_link(self):
        matches = extract_markdown_images(
            "This text has no link"
        )
        self.assertEqual(matches, [])

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
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
            ],
            new_nodes,
        )

    def test_split_images_no_image_input(self):
        node = TextNode(
            "This is text with no image.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no image.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_two_images(self):
        node = TextNode(
            "![first](url1) middle text ![second](url2) final text",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "url1"),
                TextNode(" middle text ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "url2"),
                TextNode(" final text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_at_end(self):
        node = TextNode(
            "Some text ![image](url)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Some text ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url"),
            ],
            new_nodes,
        )

    def test_split_link(self):
        pass

class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
           [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )
class TestMarkdownToBlocks(unittest.TestCase):
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
class TestBlockTypes(unittest.TestCase):
    def test_paragraph(self):
        testcases = [
            "# h1",

            "###### h6",

            """
            ```
            code
            ```
            """,

            """
            > a
            > b
            """,

            """
            - item 1
            - item 2
            """,

            """
            1. item 1
            2. item 2
            """,

            "this is a paragraph"
        ]

        testcase_results = [block_to_block_type(block.strip()) for block in testcases]
        self.assertListEqual(
            testcase_results,
            [
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.CODE,
                BlockType.QUOTE,
                BlockType.UL,
                BlockType.OL,
                BlockType.PARAGRAPH,
            ]
        )

