from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props = None):
        
        self.tag = tag
        self.value = value
        self.props = props
        super().__init__(self.tag, self.value, None, self.props)

    def __repr__(self):
        print("**********Debug**********")
        print(f'\ntag: {self.tag}\n value: {self.value}\n props: {self.props}\n')
        print("****** End of Debug *****")

    def to_html(self):
        
        if self.value == None:
        
            raise ValueError
        
        if self.tag == None:

            return self.value

        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"