import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node, node2)
  
  def test_url_eq(self):
    node = TextNode("This is a text node", TextType.BOLD, 'uri1')
    node2 = TextNode("This is a text node", TextType.BOLD, 'uri1')
    self.assertEqual(node, node2)

  def test_not_eq(self):
    node = TextNode("This is a text node", TextType.ITALIC)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertNotEqual(node, node2)

  def test_text_to_html_txt(self):
    node = TextNode("This is a text node", TextType.NORMAL)
    html_node = node.to_html_node()
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

  def test_text_to_html_text_format(self):
    node = TextNode("This is a bold node", TextType.BOLD)
    bold_node = node.to_html_node()
    self.assertEqual(bold_node.tag, 'b')
    self.assertEqual(bold_node.value, "This is a bold node")

    node1 = TextNode("This is an italic node", TextType.ITALIC)
    italic_node = node1.to_html_node()
    self.assertEqual(italic_node.tag, 'i')
    self.assertEqual(italic_node.value, "This is an italic node")
  
  def test_text_to_html_link(self):
    node = TextNode("This is a link node", TextType.LINK, 'http://url/test')
    html_node = node.to_html_node()
    self.assertEqual(html_node.tag, 'a')
    self.assertEqual(html_node.value, "This is a link node")
    self.assertIn('href', html_node.props)
    self.assertEqual(html_node.props['href'], 'http://url/test')

  def test_text_to_html_img(self):
    node = TextNode("This is an image node", TextType.IMAGE, 'url_to_image')
    html_node = node.to_html_node()
    self.assertEqual(html_node.tag, 'img')
    self.assertEqual(html_node.value, None)
    self.assertIn('src', html_node.props)
    self.assertIn('alt', html_node.props)
    self.assertEqual(html_node.props['alt'], "This is an image node")
    self.assertEqual(html_node.props['src'], "url_to_image")

if __name__ == "__main__":
  unittest.main()