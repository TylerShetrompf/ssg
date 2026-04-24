from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):

        super().__init__(tag, None, children, props)

    def to_html(self):

        if self.tag == None:
            raise ValueError("No tag on parent node")

        if self.children == None or len(self.children) == 0:
            raise ValueError("Missing children on parent node")
        
        ret_string = ""

        for child in self.children:
            
            ret_string += child.to_html()

        return f"<{self.tag}>{ret_string}</{self.tag}>"