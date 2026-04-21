import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    
    def test_eq(self):

        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC, "https://shetrompf.com")
        node4 = TextNode("This is a text node", TextType.ITALIC, "https://shetrompf.com")
        self.assertEqual(node1, node2)
        self.assertNotEqual(node2, node3)
        self.assertEqual(node3, node4)

if __name__ == "__main__":
    unittest.main