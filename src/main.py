from textnode import *
from htmlnode import HTMLNode
from leafnode import LeafNode

def main():
  node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
  print(node)

  html_node = HTMLNode('p', 'paragraph', [], {"href": "https://www.google.com", "target": "_blank"})
  print(html_node)

  print(LeafNode("p", "This is a paragraph of text.").to_html())

main()
