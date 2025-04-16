import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
  def test_no_props(self):
    node = HTMLNode('p', 'paragraph', [])
    self.assertEqual(node.props_to_html(), "")

  def test_empty_props(self):
    node = HTMLNode('p', 'paragraph', [], {})
    self.assertEqual(node.props_to_html(), "")

  def test_with_props(self):
    node = HTMLNode('p', 'paragraph', [], {"href": "https://www.google.com", "target": "_blank"})
    expected = ' href=\"https://www.google.com\" target=\"_blank\"'
    self.assertEqual(node.props_to_html(), expected)

if __name__ == "__main__":
  unittest.main()