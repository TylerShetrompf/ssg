import unittest
from markdowntoblocks import markdown_to_blocks

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

if __name__ == "__main__":
    unittest.main