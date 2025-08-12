import unittest
from textnode import TextNode, TextType
from markdownprocess import *

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

  def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )

  def test_block_to_block_type(self):
    blocks = [
      '# This is a heading',
      '### Also a heading',
      'This is a paragraph of text. It has some **bold** and _italic_ words inside of it.',
      '- This is the first list item in a list block\n- This is a list item\n- This is another list item',
      '>This is a quote\n> With multiple paragraphs',
      '- Multiple things\n>Make a normal\nparagraph',
      '1. Ordered 1\n2. Ordered 2\n3. Ordered 3',
      '1. Ordered 1\n2. Ordered 2 3. Ordered 3',
      '```Code here\n and here\n1. here```']
    
    heading_type = block_to_block_type(blocks[0])
    self.assertEqual(BlockType.HEADING, heading_type)

    heading_type2 = block_to_block_type(blocks[1])
    self.assertEqual(BlockType.HEADING, heading_type2)

    paragraph_type = block_to_block_type(blocks[2])
    self.assertEqual(BlockType.PARAGRAPH, paragraph_type)

    unordered_type = block_to_block_type(blocks[3])
    self.assertEqual(BlockType.UNORDERED_LIST, unordered_type)

    quote_type = block_to_block_type(blocks[4])
    self.assertEqual(BlockType.QUOTE, quote_type)

    paragraph_type2 = block_to_block_type(blocks[5])
    self.assertEqual(BlockType.PARAGRAPH, paragraph_type2)

    ordered_type = block_to_block_type(blocks[6])
    self.assertEqual(BlockType.ORDERED_LIST, ordered_type)

    ordered_type2 = block_to_block_type(blocks[7])
    self.assertEqual(BlockType.ORDERED_LIST, ordered_type2)

    code_type = block_to_block_type(blocks[8])
    self.assertEqual(BlockType.CODE, code_type)

  def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

  def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

  def test_lists(self):
    md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
    )

  def test_headings(self):
    md = """
# this is an h1

this is paragraph text

## this is an h2
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
    )

  def test_blockquote(self):
    md = """
> This is a
> blockquote block

this is paragraph text

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
    )

  def test_code(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

  def test_extract_title(self):
    md = "# Hello"
    result = extract_title(md)
    self.assertEqual(result, "Hello")