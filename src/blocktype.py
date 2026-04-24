from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "q"
    UNORDERED = "ul"
    ORDERED = "ol"

def block_to_block_type(markdown):

    lines = markdown.splitlines()

    quoted = True
    unordered = True
    ordered = True


    intcount = 1
    for line in lines:
        if not re.findall(r"^\>", line):
            quoted = False
        if not re.findall(r"^\- ", line):
            unordered = False
        if not re.findall(rf"^{intcount}.", line):
            ordered = False
        else:
            intcount += 1

    

    if quoted:
        return BlockType.QUOTE
    
    elif unordered:
        return BlockType.UNORDERED
    
    elif ordered:
        return BlockType.ORDERED
    
    elif re.findall(r"^\#{1,6} ", lines[0]):
        return BlockType.HEADING

    elif re.findall(r"^```", lines[0]) and re.findall("```$", lines[-1]):
        return BlockType.CODE
    
    else:
        return BlockType.PARAGRAPH