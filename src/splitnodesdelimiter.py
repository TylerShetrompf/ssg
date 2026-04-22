from textnode import TextNode, TextType

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