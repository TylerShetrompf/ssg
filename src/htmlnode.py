

class HTMLNode():


    # constructor
    def __init__(self, tag = None, value = None, children = None, props = None):
        
        self.tag = tag # string for html tag name
        self.value = value # string for value of html tag
        self.children = children # list of htmlnode child objects
        self.props = props # dict of key value pairs representing html attributes

    # debug text method
    def __repr__(self):
        print("**********Debug**********")
        print(f'\ntag: {self.tag}\n value: {self.value}\n children: {self.children}\n props: {self.props}\n')
        print("****** End of Debug *****")

    # to_html method implemented only on child classes of HTMLNode
    def to_html(self):
        
        raise NotImplementedError("to_html method implemented only on child classes of HTMLNode")
    

    # method to convert properties to HTMl
    def props_to_html(self):

        ret_string = ""

        if self.props == None or len(self.props) == 0:

            return ""

        for prop in self.props:

            ret_string += f' {prop}="{self.props[prop]}"'
        
        return ret_string