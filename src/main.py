from nodes.textnode import TextNode, TextType
from nodes.htmlnode import HTMLNode, LeafNode, ParentNode
from parser.block import markdown_to_html_node

from os import path, mkdir, listdir, makedirs
from shutil import copy, rmtree
from sys import argv

def extract_title(markdown):
    """
    Extracts a title, which in this case is defined as the first line, which should contain '# title'.
    It assumes this line is passed in.
    """
    first_line = markdown.split("\n")[0].strip()

    if not markdown.startswith("#"):
        raise ValueError("Title does not start with '#'")

    return first_line.strip("#").strip()

def generate_pages_recursive(src, template_path, dest, basepath="/"):
    """
    crawls through the directory dir, taking any markdown files and generating a page with them.
    If it encounters a directory in dir, it recursively searches it for markdown files
    """
    if not path.exists(src):
        raise OSError(f"{src} not found")
    if not path.exists(template_path):
        raise OSError(f"{template_path} not found")

    print(listdir(src))

    for file in listdir(src):
        new_src = path.join(src, file)
        new_dest = path.join(dest, file)
        if path.isfile(new_src) and new_src.endswith(".md"):
            new_dest = new_dest.rstrip(".md") + ".html"
            generate_page(new_src, template_path, new_dest, basepath)

        elif path.isdir(new_src):
            generate_pages_recursive(new_src, template_path, new_dest, basepath)

def generate_page(src, template_path, dest, basepath):
    """
    Generate page from src path to dest path using the html template at template_path
    """

    if not path.exists(src):
        raise OSError(f"{src} not found")
    if not path.exists(template_path):
        raise OSError(f"{template_path} not found")
        
    print(f"Generating page from {src} to {dest} using {template_path}")

    f_from = open(src, 'r')
    markdown = f_from.read()
    f_from.close()

    f_template = open(template_path, 'r')
    content = f_template.read()
    f_template.close()

    content = content.replace("{{ Title }}", extract_title(markdown))
    content = content.replace("{{ Content }}", markdown_to_html_node(markdown).to_html())
    content = content.replace("href=\"/", f"href=\"{basepath}")
    content = content.replace("src=\"/", f"src=\"{basepath}")

    parent_path = "/".join(dest.split("/")[:-1])
    if not path.exists(parent_path):
        makedirs(parent_path)

    with open(dest, 'w+') as f_dest:
        f_dest.write(content)

def publish(src="static", dest="public"):
    """
    Takes a source and destination filepath string. recursively copies files from src to dest.
    """

    src = path.abspath(src)
    dest = path.abspath(dest)

    if not path.exists(src):
        raise OSError(f"{src} not found")

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
    argc = len(argv)
    if argc < 2:
        basepath = "/"
    elif argc == 2:
        basepath = argv[1]
    else:
        raise ValueError("Only accepts 0 or 1 arguments")

    publish()
    generate_pages_recursive("content", "layouts/template.html", "docs", basepath)

if __name__ == "__main__":
    main()
