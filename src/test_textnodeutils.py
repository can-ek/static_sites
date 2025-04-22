import unittest
from textnode import TextNode, TextType
from textnodeutils import *

class TestTextNodeUtils(unittest.TestCase):

  def test_extract_markdown_images(self):
    matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

  def test_extract_markdown_link(self):
    matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
    self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

  def test_split_links(self):
    node = TextNode(
       "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) two links",
      TextType.NORMAL,
    )

    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
          TextNode("This is text with a link ", TextType.NORMAL),
          TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
          TextNode(" and ", TextType.NORMAL),
          TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
          TextNode(" two links", TextType.NORMAL)
        ],
        new_nodes
    )

  def test_split_images(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
      TextType.NORMAL,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.NORMAL),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.NORMAL),
        TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
      ],
      new_nodes,
    )

  def test_split_images_and_links(self):
    node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [to youtube](https://www.youtube.com/@bootdotdev) as a link", TextType.NORMAL,)
    
    new_nodes = split_nodes_image([node])

    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.NORMAL),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and [to youtube](https://www.youtube.com/@bootdotdev) as a link", TextType.NORMAL)
      ],
      new_nodes,
    )

    new_nodes_2 = split_nodes_link(new_nodes)
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.NORMAL),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and ", TextType.NORMAL),
        TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        TextNode(" as a link", TextType.NORMAL)
      ],
      new_nodes_2,
    )

  def test_text_to_textnode(self):
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    node_list = text_to_textnodes(text)

    self.assertListEqual(
      [
        TextNode("This is ", TextType.NORMAL),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.NORMAL),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.NORMAL),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.NORMAL),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.NORMAL),
        TextNode("link", TextType.LINK, "https://boot.dev"),
      ],
      node_list
    )