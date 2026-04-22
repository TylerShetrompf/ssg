def markdown_to_blocks(markdown):
    
    blocks = markdown.split("\n\n")
    
    ret_blocks = []
    
    for i in range(len(blocks)):
        
        blocks[i] = blocks[i].strip()
        
        if blocks[i] != "":
        
            ret_blocks.append(blocks[i])
    
    return ret_blocks