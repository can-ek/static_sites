import re
from textnode import TextType, TextNode

def extract_markdown_images(text):
  pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(pattern, text)
  return matches

def extract_markdown_links(text):
  pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(pattern, text)
  return matches

def split_by_pattern(text_type, pattern, extract_function):
  def internal_func(old_nodes):
    new_nodes = []
    for node in old_nodes:
      if node.text_type == TextType.NORMAL:
        items = extract_function(node.text)
        text = node.text
        for item in items:
          format_pattern = pattern.format(text = item[0], url = item[1])
          text_parts = text.split(format_pattern)
          new_nodes.append(TextNode(text_parts[0], TextType.NORMAL))
          new_nodes.append(TextNode(item[0], text_type, item[1]))
          text = text_parts[1]
        
        if len(text) > 0:
          new_nodes.append(TextNode(text, TextType.NORMAL))
      else:
        new_nodes.append(node)
    return new_nodes
  return internal_func

split_nodes_image = split_by_pattern(TextType.IMAGE, "![{text}]({url})", extract_markdown_images)
split_nodes_link = split_by_pattern(TextType.LINK, "[{text}]({url})", extract_markdown_links)

def text_to_textnodes(text):
  initial_node = TextNode(text, TextType.NORMAL)
  nodes_delimiter_b = TextNode.split_nodes_delimiter([initial_node], '**', TextType.BOLD)
  nodes_delimiter_bi = TextNode.split_nodes_delimiter(nodes_delimiter_b, '_', TextType.ITALIC)
  nodes_delimiter_bic = TextNode.split_nodes_delimiter(nodes_delimiter_bi, '`', TextType.CODE)
  nodes_imgs = split_nodes_image(nodes_delimiter_bic)
  final_nodes = split_nodes_link(nodes_imgs)
  return final_nodes