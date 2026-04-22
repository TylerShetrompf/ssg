import unittest
from textnode import TextNode, TextType
from texttotextnode import text_to_textnodes

class TestTextToTextNode(unittest.TestCase):
    
    def test_multi_string(self):
        result = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        desired = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(result, desired)

    def test_empty_string(self):
        result = text_to_textnodes("")
        desired = []
        self.assertListEqual(result, desired)

    def test_no_delimiters(self):
        result = text_to_textnodes("This is a plain string with no special formatting.")
        desired = [TextNode("This is a plain string with no special formatting.", TextType.TEXT)]
        self.assertListEqual(result, desired)

    def test_only_bold(self):
        result = text_to_textnodes("**Bold text only**")
        desired = [TextNode("Bold text only", TextType.BOLD)]
        self.assertListEqual(result, desired)

    def test_only_italic(self):
        result = text_to_textnodes("_Italic text only_")
        desired = [TextNode("Italic text only", TextType.ITALIC)]
        self.assertListEqual(result, desired)

    def test_only_code(self):
        result = text_to_textnodes("`Code block only`")
        desired = [TextNode("Code block only", TextType.CODE)]
        self.assertListEqual(result, desired)

    def test_only_image(self):
        result = text_to_textnodes("![alt text](url)")
        desired = [TextNode("alt text", TextType.IMAGE, "url")]
        self.assertListEqual(result, desired)

    def test_only_link(self):
        result = text_to_textnodes("[link text](link_url)")
        desired = [TextNode("link text", TextType.LINK, "link_url")]
        self.assertListEqual(result, desired)

    def test_consecutive_delimiters(self):
        result = text_to_textnodes("**bold****more bold**_italic__more italic_`code``more code`")
        desired = [
            TextNode("bold", TextType.BOLD),
            TextNode("more bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("more italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("more code", TextType.CODE),
        ]
        self.assertListEqual(result, desired)

    def test_mixed_delimiters_no_text(self):
        result = text_to_textnodes("**bold**_italic_`code`")
        desired = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(result, desired)

    def test_delimiters_at_start_and_end(self):
        result = text_to_textnodes("**Start bold** text in middle **End bold**")
        desired = [
            TextNode("Start bold", TextType.BOLD),
            TextNode(" text in middle ", TextType.TEXT),
            TextNode("End bold", TextType.BOLD),
        ]
        self.assertListEqual(result, desired)
        
        result = text_to_textnodes("_Start italic_ text in middle _End italic_")
        desired = [
            TextNode("Start italic", TextType.ITALIC),
            TextNode(" text in middle ", TextType.TEXT),
            TextNode("End italic", TextType.ITALIC),
        ]
        self.assertListEqual(result, desired)

        result = text_to_textnodes("`Start code` text in middle `End code`")
        desired = [
            TextNode("Start code", TextType.CODE),
            TextNode(" text in middle ", TextType.TEXT),
            TextNode("End code", TextType.CODE),
        ]
        self.assertListEqual(result, desired)

    def test_unclosed_delimiter(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This is **unclosed bold text")
        with self.assertRaises(ValueError):
            text_to_textnodes("This is _unclosed italic text")
        with self.assertRaises(ValueError):
            text_to_textnodes("This is `unclosed code text")


if __name__ == '__main__':
    unittest.main()