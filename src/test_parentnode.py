import unittest

from parentnode import ParentNode
from leafnode import LeafNode

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
