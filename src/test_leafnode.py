import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
  def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

  def test_leaf_to_html_a(self):
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

  def test_leaf_to_html_no_tag(self):
    node = LeafNode(None, "Click me!")
    self.assertEqual(node.to_html(), "Click me!")

  def test_leaf_to_html_no_value(self):
    node = LeafNode('a', None)
    with self.assertRaises(ValueError) as cm:
      node.to_html()

    self.assertEqual(type(cm.exception), ValueError)
    self.assertEqual(cm.exception.args[0], "Missing value")

if __name__ == "__main__":
  unittest.main()