from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    # constructor
    def __init__(self, tag, value, props = None):

        super().__init__(tag, value, None, props)

    # method for debug text
    def __repr__(self):
        print("**********Debug**********")
        print(f'\ntag: {self.tag}\n value: {self.value}\n props: {self.props}\n')
        print("****** End of Debug *****")

    # method for converting node value and tag to html. calls parent method props_to_html
    def to_html(self):
        
        if self.value == None:
        
            raise ValueError("No value on leaf node")
        
        if self.tag == None:

            return self.value

        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"