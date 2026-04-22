import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode
from splitnodesdelimiter import split_nodes_delimiter

class TestSplitNodeDelimeter(unittest.TestCase):

    def test_text(self):
        node = TextNode("this is a plain text node", TextType.TEXT, None)
        returnnode = split_nodes_delimiter([node], None, TextType.TEXT)
        self.assertEqual(node.text_type, returnnode[0].text_type)

    def test_code(self):
        node = TextNode("this is a `code text` node", TextType.TEXT, None)
        returnnode = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(returnnode[1].text_type, TextType.CODE)

    def test_bold(self):
        node = TextNode("this is a **bold text** node", TextType.TEXT, None)
        returnnode = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(returnnode[1].text_type, TextType.BOLD)
    
    def test_italic(self):
        node = TextNode("this is an _italic text_ node", TextType.TEXT, None)
        returnnode = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(returnnode[1].text_type, TextType.ITALIC)

    def test_multiple_delimiters(self):
        node = TextNode("This is a `code` and another `code` snippet.", TextType.TEXT, None)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[3].text, "code")

    def test_delimiter_at_start_and_end(self):
        node = TextNode("`code at start` and `code at end`", TextType.TEXT, None)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text_type, TextType.CODE)
        self.assertEqual(new_nodes[0].text, "code at start")
        self.assertEqual(new_nodes[2].text, "code at end")

    def test_no_delimiter(self):
        node = TextNode("This text has no delimiters.", TextType.TEXT, None)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "This text has no delimiters.")

    def test_empty_string(self):
        node = TextNode("", TextType.TEXT, None)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "")

    def test_only_delimiter(self):
        node = TextNode("` `", TextType.TEXT, None)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
    
    def test_delimiter_in_middle_of_word(self):
        node = TextNode("word`code`word", TextType.TEXT, None)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "word")
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[2].text, "word")

    def test_nested_delimiters(self):
        node = TextNode("This is **_bold and italic_** text.", TextType.TEXT, None)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "_bold and italic_") # Delimiter not handled by this function
    

if __name__ == '__main__':
    unittest.main()