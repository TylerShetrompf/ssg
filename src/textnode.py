from enum import Enum
from leafnode import LeafNode

# enum class for text types conversion
class TextType(Enum):
    TEXT = ""
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINK = "a"
    IMAGE = "img"

# textnode class for storing text data
class TextNode():
    
    # constructor
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    # method for handling == operations
    def __eq__(self, target):
        if self.text == target.text and self.text_type == target.text_type and self.url == target.url:
            return True
    
    # method for debug text
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

# function for converting text node to html leaf node
def text_node_to_html_node(text_node):
    
    # raise exception if text_node.text_type not in TextType
    if text_node.text_type not in TextType:
        raise Exception("text type of text node not in TextType")

    if text_node.text_type == TextType.TEXT:
        new_node = LeafNode(None, text_node.text, None)
        return new_node
    
    if text_node.text_type in [TextType.ITALIC, TextType.BOLD, TextType.CODE]: 
        new_node = LeafNode(text_node.text_type.value, text_node.text, None)
        return new_node

    if text_node.text_type == TextType.LINK:
        new_node = LeafNode(text_node.text_type.value, text_node.text, {"href": text_node.url})
        return new_node
    
    if text_node.text_type == TextType.IMAGE:
        new_node = LeafNode(text_node.text_type.value, None, {"src": text_node.url, "alt": text_node.text})
        return new_node