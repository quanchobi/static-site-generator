from nodes.textnode import TextNode, TextType
from nodes.htmlnode import HTMLNode, LeafNode, ParentNode

from os import path, mkdir, listdir
from shutil import copy, rmtree

def publish(src="static", dest="public"):
    """
    Takes a source and destination filepath string. recursively copies files from src to dest.
    """

    src = path.abspath(src)
    dest = path.abspath(dest)

    if not path.exists(src):
        raise OSError("file not found")

    if path.exists(dest):
         rmtree(dest)

    mkdir(dest)

    for file in listdir(src):
        src_fp = path.join(src, file)
        dest_fp = path.join(dest, file)

        if path.isfile(src_fp):
            copy(src_fp, dest_fp)
        elif path.isdir(src_fp):
            publish(src_fp, dest_fp)

def main():
    publish()

if __name__ == "__main__":
    main()
