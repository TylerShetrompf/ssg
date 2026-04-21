import unittest

from htmlnode import HTMLNode

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

