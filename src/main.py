from textnode import *
from htmlnode import HTMLNode

def main():
  node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
  print(node)

  html_node = HTMLNode('p', 'paragraph', [], {"href": "https://www.google.com", "target": "_blank"})
  print(html_node)

main()
