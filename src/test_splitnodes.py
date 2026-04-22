import unittest
from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link

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
    
class TestSplitNodeImage(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_no_image(self):
        node = TextNode("This text has no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_image_at_start(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) This is text.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" This is text.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_multiple_images_no_text_in_between(self):
        node = TextNode("![image1](url1)![image2](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "url1"),
                TextNode("image2", TextType.IMAGE, "url2"),
            ],
            new_nodes,
        )

    def test_image_with_empty_alt_text(self):
        node = TextNode("Text with an ![](/path/to/image.png) image.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with an ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "/path/to/image.png"),
                TextNode(" image.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_only_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes,
        )

class TestSplitNodeLink(unittest.TestCase):

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.google.com"
                ),
            ],
            new_nodes,
        )
    
    def test_no_link(self):
        node = TextNode("This text has no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_link_at_start(self):
        node = TextNode("[link](https://www.example.com) This is text.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" This is text.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_end(self):
        node = TextNode("This is text with a [link](https://www.example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
        )

    def test_multiple_links_no_text_in_between(self):
        node = TextNode("[link1](url1)[link2](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "url1"),
                TextNode("link2", TextType.LINK, "url2"),
            ],
            new_nodes,
        )

    def test_link_with_empty_text(self):
        node = TextNode("Text with a [](/path/to/page) link.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with a ", TextType.TEXT),
                TextNode("", TextType.LINK, "/path/to/page"),
                TextNode(" link.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_only_link(self):
        node = TextNode("[link](https://www.example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://www.example.com")],
            new_nodes,
        )

if __name__ == '__main__':
    unittest.main()