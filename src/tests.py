import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links
from htmlnode import HTMLNode
from leafnode import LeafNode
from markdowntoblocks import markdown_to_blocks
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from texttotextnode import text_to_textnodes
from blocktype import BlockType, block_to_block_type
from blocktohtml import markdown_to_html_node
from main import extract_title

# Extract Markdown
class TestExtractMarkdown(unittest.TestCase):
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to shetrompf.com](https://shetrompf.com) and [to youtube](https://www.youtube.com/)"
        )
        self.assertListEqual([("to shetrompf.com", "https://shetrompf.com"), ("to youtube", "https://www.youtube.com/")], matches)

    def test_extract_markdown_images_no_images(self):
        matches = extract_markdown_images(
            "This is text with no images."
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_no_links(self):
        matches = extract_markdown_links(
            "This is text with no links."
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with ![image1](https://example.com/img1.png) and ![image2](https://example.com/img2.jpg) and ![image3](https://example.com/img3.gif)"
        )
        self.assertListEqual([("image1", "https://example.com/img1.png"), ("image2", "https://example.com/img2.jpg"), ("image3", "https://example.com/img3.gif")], matches)

    def test_extract_markdown_links_multiple_links(self):
        matches = extract_markdown_links(
            "Here are [link1](https://link1.com), [link2](https://link2.org), and [link3](https://link3.net)."
        )
        self.assertListEqual([("link1", "https://link1.com"), ("link2", "https://link2.org"), ("link3", "https://link3.net")], matches)

    def test_extract_markdown_images_empty_string(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_empty_string(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_inline_text(self):
        matches = extract_markdown_images("Text before ![img](http://url) text after.")
        self.assertListEqual([("img", "http://url")], matches)

    def test_extract_markdown_links_inline_text(self):
        matches = extract_markdown_links("Text before [link](http://url) text after.")
        self.assertListEqual([("link", "http://url")], matches)
    
    def test_extract_markdown_images_no_alt_text(self):
        matches = extract_markdown_images("This is an image with no alt text ![](https://example.com/image.png)")
        self.assertListEqual([("", "https://example.com/image.png")], matches)

    def test_extract_markdown_images_special_chars_in_alt_text(self):
        matches = extract_markdown_images("An image with special chars ![Im@ge W!th Sp3ci@l Ch@rs](https://example.com/special.png)")
        self.assertListEqual([("Im@ge W!th Sp3ci@l Ch@rs", "https://example.com/special.png")], matches)

    def test_extract_markdown_links_special_chars_in_link_text(self):
        matches = extract_markdown_links("A link with special chars [L!nk W!th Sp3ci@l Ch@rs](https://example.com/special-link)")
        self.assertListEqual([("L!nk W!th Sp3ci@l Ch@rs", "https://example.com/special-link")], matches)

    def test_extract_markdown_images_whitespace_in_url(self):
        matches = extract_markdown_images("Image with whitespace ![image](https://example.com/path with spaces/image.png)")
        self.assertListEqual([("image", "https://example.com/path with spaces/image.png")], matches)

    def test_extract_markdown_links_whitespace_in_url(self):
        matches = extract_markdown_links("Link with whitespace [link](https://example.com/path with spaces/link)")
        self.assertListEqual([("link", "https://example.com/path with spaces/link")], matches)

# HTML Node 
class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):

        props1 = {
            "href": "https://shetrompf.com",
            "target": "_blank" 
            }
        
        props2 = {
            "href": "https://shetrompf.com",
            "target": "_blank" 
            }
        
        props3 = {
            "href": "https://tyler.shetrompf.com",
            "target": "_blank" 
            }
        
        props4 = {}

        node1 = HTMLNode("h1", "This is a test", None, props1)
        node2 = HTMLNode("h1", "This is a test", None, props2)
        node3 = HTMLNode("h1", "This is a test", None, props3)
        node4 = HTMLNode("h1", "This is a test", None, props4)

        self.assertEqual(node1.props, node2.props)
        self.assertNotEqual(node2.props, node3.props)
        self.assertNotEqual(node3.props, node4.props)

# Leaf Node
class TestLeafNode(unittest.TestCase):

    def test_debug_prints(self):
        node1 = LeafNode("p", "Hello, world!")
        node2 = LeafNode("a", "Take me home Scottie", {"href": "https://shetrompf.com"})
        node1.__repr__
        node2.__repr__

    
    def test_leaf_to_html_p(self):
        
        node1 = LeafNode("p", "Hello, world!")
        self.assertEqual(node1.to_html(), "<p>Hello, world!</p>")
        self.assertNotEqual(node1.to_html(), '<a href="https://shetrompf.com"> Take me home Scottie a>')


    def test_leaf_to_html_a(self):
        
        node2 = LeafNode("a", "Take me home Scottie", {"href": "https://shetrompf.com"})
        self.assertEqual(node2.to_html(), '<a href="https://shetrompf.com">Take me home Scottie</a>')
        self.assertNotEqual(node2.to_html(), '<a href="https://shetrompf.com"> Take me home Scottie a>')

# Markdown to Blocks
class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_with_only_newlines(self):
        md = "\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_multiple_consecutive_newlines(self):
        md = """
Paragraph one


Paragraph two


Paragraph three
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Paragraph one",
                "Paragraph two",
                "Paragraph three",
            ],
        )

    def test_leading_trailing_newlines(self):
        md = """

Paragraph with leading and trailing newlines

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Paragraph with leading and trailing newlines",
            ],
        )

    def test_various_block_types(self):
        md = """
# Heading one

This is a paragraph.

```
Code block
line 2
```

> Quote block
> line 2

- List item 1
- List item 2

1. Numbered list item 1
2. Numbered list item 2
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading one",
                "This is a paragraph.",
                "```\nCode block\nline 2\n```",
                "> Quote block\n> line 2",
                "- List item 1\n- List item 2",
                "1. Numbered list item 1\n2. Numbered list item 2",
            ],
        )

    def test_mixed_content_with_empty_lines(self):
        md = """
# Heading

Paragraph one.


Paragraph two.

- List item 1
- List item 2


```
Code here
```
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph one.",
                "Paragraph two.",
                "- List item 1\n- List item 2",
                "```\nCode here\n```",
            ],
        )

#Parent Node
class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_to_html_with_none_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "text")]).to_html()

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("p", "paragraph")
        child2 = LeafNode("span", "span text")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), "<div><p>paragraph</p><span>span text</span></div>")

    def test_to_html_with_complex_children(self):
        grandchild1 = LeafNode("b", "bold text")
        grandchild2 = LeafNode("i", "italic text")
        child1 = ParentNode("span", [grandchild1, grandchild2])
        child2 = LeafNode("a", "link", {"href": "https://example.com"})
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), '<div><span><b>bold text</b><i>italic text</i></span><a href="https://example.com">link</a></div>')

    def test_to_html_with_children_no_value(self):
        child_node = LeafNode("span", None)
        parent_node = ParentNode("div", [child_node])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_none_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

# Splitting Nodes
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

    def test_empty_string_link(self):
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

# Text Node
class TestTextNode(unittest.TestCase):
    
    def test_eq(self):

        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC, "https://shetrompf.com")
        node4 = TextNode("This is a text node", TextType.ITALIC, "https://shetrompf.com")
        self.assertEqual(node1, node2)
        self.assertNotEqual(node2, node3)
        self.assertEqual(node3, node4)

# Text Node to HTML Node
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text")

    def test_italic_text(self):
        node = TextNode("This is an italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text")

    def test_code_text(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    def test_link_text(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image_text(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "This is an image"})

# Text to Text Node
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

# Block type
class TestBlockType(unittest.TestCase):

    def test_block_unordered(self):

        res = block_to_block_type("- This is a list\n- with items",)

        self.assertEqual(BlockType.UNORDERED, res)
    
    def test_block_ordered(self):
        
        res = block_to_block_type("1. This is an ordered list\n2. with items")
        
        self.assertEqual(BlockType.ORDERED, res)

    def test_block_paragraph(self):
        
        res = block_to_block_type("This is a regular paragraph.")

        self.assertEqual(BlockType.PARAGRAPH, res)

    def test_block_code(self):

        res = block_to_block_type("```\nThis is a code block\nwith multiple lines\n```")
        
        self.assertEqual(BlockType.CODE, res)

    def test_block_heading(self):

        res = block_to_block_type("# This is a heading block\n## with multiple header levels\n### like this")
        
        self.assertEqual(BlockType.HEADING, res)

    def test_block_quote(self):

        res = block_to_block_type("> this is a \n> multi-line\n> quoted block")

        self.assertEqual(BlockType.QUOTE, res)

# Block to HTML
class TestBlockToHTML(unittest.TestCase):
    def test_markdown_to_html_node_paragraph(self):
        markdown = "This is a paragraph."
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><p>This is a paragraph.</p></div>")

    def test_markdown_to_html_node_code(self):
        markdown = """```
print('Hello, world!')```"""
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><pre><code>print('Hello, world!')</code></pre></div>")

    def test_markdown_to_html_node_quote(self):
        markdown = """> This is a quote.
> Second line."""
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><blockquote>This is a quote. Second line. </blockquote></div>")

    def test_markdown_to_html_node_unordered_list(self):
        markdown = """- Item 1
- Item 2"""
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>")

    def test_markdown_to_html_node_ordered_list(self):
        markdown = """1. First item
2. Second item"""
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><ol><li>First item</li><li>Second item</li></ol></div>")

# Header extraction
class TestExtractTitle(unittest.TestCase):
    
    def test_header_with_trailing_white(self):
        md = """# this is a header
this is not
this is also not
this has some trailing white space   """
        res = extract_title(md)
        self.assertEqual("this is a header", res)

    def test_no_header(self):
        md = """ this test has no header
but it does have
multiple lines"""
        self.assertRaises(Exception, extract_title(md))

if __name__ == '__main__':
    unittest.main()