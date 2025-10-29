def markdown_to_blocks(markdown):
    """
    Takes a raw markdown string and returns a list of blocks
    """
    blocks = markdown.split("\n\n")

    return list(filter(None, (b.strip() for b in blocks)))

