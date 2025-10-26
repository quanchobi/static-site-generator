#!/urs/bin/env python3
from src.nodes.textnode import TextNode, TextType
from src.nodes.htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    textnode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(textnode)

if __name__ == "__main__":
    main()
