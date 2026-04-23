from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "q"
    UNORDERED = "ul"
    ORDERED = "ol"

