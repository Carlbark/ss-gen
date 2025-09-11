from textnode import TextNode, TextType


def main():
    print("Hello world")
    textnode = TextNode("This is some anchor text", TextType.LINK, "https://example.com")
    print(textnode)

main()