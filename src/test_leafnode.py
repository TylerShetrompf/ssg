import unittest

from leafnode import LeafNode

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
