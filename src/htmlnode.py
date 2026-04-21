

class HTMLNode():

    def __init__(self, tag = None, value = None, children = None, props = None):
        
        self.tag = tag # string for html tag name
        self.value = value # string for value of html tag
        self.children = children # list of htmlnode child objects
        self.props = props # dict of key value pairs representing html attributes

    def __repr__(self):
        print("**********Debug**********")
        print(f'\ntag: {self.tag}\n value: {self.value}\n children: {self.children}\n props: {self.props}\n')
        print("****** End of Debug *****")


    def to_html(self):
        
        raise NotImplementedError("to_html method implemented only on child classes of HTMLNode")
    
    def props_to_html(self):

        ret_string = ""

        if self.props == None or len(self.props) == 0:

            return ""

        for prop in self.props:

            ret_string += f' {prop}="{self.props[prop]}"'
        
        return ret_string