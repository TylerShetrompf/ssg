from htmlnode import HTMLNode
from markdowntoblocks import markdown_to_blocks
from blocktype import block_to_block_type, BlockType
from parentnode import ParentNode
from texttotextnode import text_to_textnodes, TextNode, TextType
from textnode import text_node_to_html_node

def text_to_children(block):
    
    textnodes = text_to_textnodes(block)

    htmlnodes = []

    for node in textnodes:

        htmlnodes.append(text_node_to_html_node(node))
    
    return htmlnodes


#function to determine h level of heading
def heading_level(block):
    count = 0
    for c in block:
        if c == "#":
            count +=1
        else:
            break
    return count

def markdown_to_html_node(markdown):

    # convert the markdown to blocks
    blocks = markdown_to_blocks(markdown)
    
    #list to hold children
    children = []
   
    for block in blocks:

        bt = block_to_block_type(block)

        match bt:

            case BlockType.PARAGRAPH:

                rep_text = block.replace("\n", " ")
                
                block_children = text_to_children(rep_text)

                node = ParentNode("p", block_children)

                children.append(node)
            
            case BlockType.HEADING:
                
                block_children = []

                strip_text = ""

                lines = block.splitlines()
                
                for line in lines:

                    strip_text += line.lstrip("# ")

                block_children = text_to_children(strip_text)
                
                tag = "h" + str(heading_level(block))

                node = ParentNode(tag, block_children)

                children.append(node)

            case BlockType.CODE:

                strip_text = block[4:]
                strip_text = strip_text[:-3]

                # text to text node
                t_node = TextNode(strip_text, TextType.TEXT)

                h_node = text_node_to_html_node(t_node)

                # textnodes inside of code node
                c_node = ParentNode("code", [h_node])

                # code node inside of pre node
                p_node = ParentNode("pre", [c_node])

                children.append(p_node)

            case BlockType.QUOTE:
                
                lines = block.splitlines()
                strip_text = ""
                for line in lines:
                    strip_text += f"{line[2:]} "

                block_children = text_to_children(strip_text)

                node = ParentNode("blockquote", block_children)

                children.append(node)
            
            case BlockType.UNORDERED:

                lines = block.splitlines()

                li_children = []

                for line in lines:

                    strip_line = line.lstrip("- ")

                    text_node = text_to_children(strip_line)

                    html_Node = ParentNode("li", text_node)

                    li_children.append(html_Node)                
                
                p_node = ParentNode("ul", li_children)

                children.append(p_node)

            case BlockType.ORDERED:

                lines = block.splitlines()

                li_children = []

                for line in lines:

                    strip_line = line[3:]

                    text_node = text_to_children(strip_line)

                    html_Node = ParentNode("li", text_node)

                    li_children.append(html_Node)                
                
                p_node = ParentNode("ol", li_children)

                children.append(p_node)
    
    parent = ParentNode("div", children, None)

    return parent

