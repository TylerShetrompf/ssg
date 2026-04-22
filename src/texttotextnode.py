from splitnodes import split_nodes_link, split_nodes_delimiter, split_nodes_image
from textnode import TextNode, TextType

def text_to_textnodes(text):
    if not text:
        return []

    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes