import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links

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

if __name__ == '__main__':
    unittest.main()
