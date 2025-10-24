#!/usr/bin/env python3

import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ineq_text(self):
        node = TextNode("This is a foo node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_ineq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_ineq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://foo.bar")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://foo.baz")
        self.assertNotEqual(node, node2)

    def test_bad_text_type(self):
        with self.assertRaises(ValueError):
            TextNode("bad type", "BOLD")

    def test_wrong_enum_type(self):
        class FakeType: pass
        with self.assertRaises(ValueError):
            TextNode("bad type", FakeType())

if __name__ == "__main__":
    unittest.main()
