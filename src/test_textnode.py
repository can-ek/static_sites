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

  #region to_html_node()
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
  #endregion

  #region split_nodes_delimiter()
  def test_single_node_to_code(self):
    node = TextNode("This is text with a `code block` word", TextType.NORMAL)
    new_nodes = TextNode.split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertListEqual(new_nodes, [
      TextNode("This is text with a ", TextType.NORMAL),
      TextNode("code block", TextType.CODE),
      TextNode(" word", TextType.NORMAL)
    ])

  def test_single_node_multiple_delimiter(self):
    node = TextNode("Normal **bold txt** normal _italic_ normal", TextType.NORMAL)
    new_nodes = TextNode.split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = TextNode.split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

    self.assertListEqual(new_nodes, [
      TextNode("Normal ", TextType.NORMAL),
      TextNode("bold txt", TextType.BOLD),
      TextNode(" normal ", TextType.NORMAL),
      TextNode("italic", TextType.ITALIC),
      TextNode(" normal", TextType.NORMAL)
    ])

  def test_single_node_starts_and_ends_delimited(self):
    node = TextNode("_italic txt_ normal _italic_", TextType.NORMAL)
    new_nodes = TextNode.split_nodes_delimiter([node], "_", TextType.ITALIC)
    self.assertListEqual(new_nodes, [
      TextNode("italic txt", TextType.ITALIC),
      TextNode(" normal ", TextType.NORMAL),
      TextNode("italic", TextType.ITALIC)
    ])

  def test_multiple_nodes_single_delimiter(self):
    node1 = TextNode("Text _italic_ text", TextType.NORMAL)
    node2 = TextNode("Text2 _italic2_ text2", TextType.NORMAL)
    new_nodes = TextNode.split_nodes_delimiter([node1, node2], "_", TextType.ITALIC)
    self.assertListEqual(new_nodes, [
      TextNode("Text ", TextType.NORMAL),
      TextNode("italic", TextType.ITALIC),
      TextNode(" text", TextType.NORMAL),
      TextNode("Text2 ", TextType.NORMAL),
      TextNode("italic2", TextType.ITALIC),
      TextNode(" text2", TextType.NORMAL)
    ])
  
  #endregion

if __name__ == "__main__":
  unittest.main()