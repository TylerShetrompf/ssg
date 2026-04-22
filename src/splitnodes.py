from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links

# function to split node into multiple nodes given a delimiter
def split_nodes_delimiter(old_nodes, delimiter, text_type):

    if delimiter == None:
        return old_nodes
    
    ret_list = []
    
    for node in old_nodes:

        if node.text_type == TextType.TEXT:
            
            if delimiter not in node.text:

                ret_list.append(TextNode(node.text, TextType.TEXT))
            
            else:
                
                split_array = node.text.split(delimiter)

                if len(split_array) % 2 != 1:

                    raise Exception("Invalid markdown syntax, missing closing delimiter")
                
                else:
                    
                    for i in range(len(split_array)):

                        if split_array[i] == "":
                            continue
                        
                        elif i % 2 == 0:
                            
                            ret_list.append(TextNode(split_array[i], TextType.TEXT))

                        else:

                            ret_list.append(TextNode(split_array[i], text_type))

        else:

            ret_list.append(node)

    return ret_list

def split_nodes_image(old_nodes):

    ret_list = []

    for node in old_nodes:

        matched_image_text = extract_markdown_images(node.text)

        if len(matched_image_text) == 0:
            
            ret_list.append(node)

        else:
            
            remaining_text = node.text
            
            for i in range(len(matched_image_text)):
                
                image_alt = matched_image_text[i][0]
                image_link = matched_image_text[i][1]
                
                split_text = remaining_text.split(f"![{image_alt}]({image_link})", maxsplit = 1)
                
                if split_text[0] != "":
                    ret_list.append(TextNode(split_text[0], TextType.TEXT, None))
                
                ret_list.append(TextNode(image_alt, TextType.IMAGE, image_link))
                
                remaining_text = split_text[1]
            
            if remaining_text != "":

                ret_list.append(TextNode(remaining_text, TextType.TEXT, None))
                
    return ret_list

def split_nodes_link(old_nodes):

    ret_list = []

    for node in old_nodes:

        matched_link_text = extract_markdown_links(node.text)

        if len(matched_link_text) == 0:
            
            ret_list.append(node)

        else:
            
            remaining_text = node.text
            
            for i in range(len(matched_link_text)):
                
                link_text = matched_link_text[i][0]
                link_url = matched_link_text[i][1]
                
                split_text = remaining_text.split(f"[{link_text}]({link_url})", maxsplit = 1)
                
                if split_text[0] != "":
                    ret_list.append(TextNode(split_text[0], TextType.TEXT, None))
                
                ret_list.append(TextNode(link_text, TextType.LINK, link_url))
                
                remaining_text = split_text[1]
            
            if remaining_text != "":

                ret_list.append(TextNode(remaining_text, TextType.TEXT, None))
                
    return ret_list