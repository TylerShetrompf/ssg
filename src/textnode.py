from enum import Enum

# enum class for text types conversion
class TextType(Enum):
    TEXT = "text (plain)"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

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