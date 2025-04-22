from enum import Enum
import re
from leafnode import LeafNode

class TextType(Enum):
  NORMAL = 'normal'
  BOLD = 'bold'
  ITALIC = 'italic'
  CODE = 'code'
  LINK = 'link'
  IMAGE = 'image'

class TextNode:
  def __init__(self, text, text_type: TextType, url = None):
    self.text = text
    self.text_type = text_type
    self.url = url

  def __eq__(self, other):
    return self.text == other.text and self.text_type == other.text_type and self.url == other.url
  
  def __repr__(self):
    return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
  
  def to_html_node(self):
    match (self.text_type):
      case (TextType.NORMAL):
        return LeafNode(None, self.text)
      case (TextType.BOLD):
        return LeafNode('b', self.text)
      case (TextType.ITALIC):
        return LeafNode('i', self.text)
      case (TextType.CODE):
        return LeafNode('code', self.text)
      case (TextType.LINK):
        return LeafNode('a', self.text, {'href': self.url})
      case (TextType.IMAGE):
        return LeafNode('img', None, {'src': self.url, 'alt': self.text})
      case _:
        raise Exception('Invalid text type')
      
  def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
      split_text = node.text.split(delimiter)
      
      # If the string begins with a delimiter, words affected by the delimiter are in odd possitions
      # pick the first word and start from the first not-affected word
      if split_text[0] == '':
        new_node = TextNode(split_text[1], text_type)
        new_nodes.append(new_node)
        split_text = split_text[2:]

      # If the last character is an empty string, ignore it
      if split_text[-1] == '':
        split_text = split_text[0:-1]

      # otherwise, the words affected by the delimiter are in even possitions, start from the beginning
      for i in range(0, len(split_text)):
        new_node = TextNode(split_text[i], node.text_type if i % 2 == 0 else text_type)
        new_nodes.append(new_node)
      
    return new_nodes
