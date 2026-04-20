from textnode import TextNode,TextType

# test case
def main():
    test_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(test_node.__repr__())

main()