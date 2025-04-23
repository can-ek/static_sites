import re
from textnode import TextType, TextNode
from blocktype import BlockType

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
  """
  Function used to parse a block of text into multiple TextNode instances using the correct formatting

  Parameters
  -------
  text : str
    A block of markdown text

  Returns
  -------
  list:
    A list of TextNode instances
  """
  initial_node = TextNode(text, TextType.NORMAL)
  nodes_delimiter_b = TextNode.split_nodes_delimiter([initial_node], '**', TextType.BOLD)
  nodes_delimiter_bi = TextNode.split_nodes_delimiter(nodes_delimiter_b, '_', TextType.ITALIC)
  nodes_delimiter_bic = TextNode.split_nodes_delimiter(nodes_delimiter_bi, '`', TextType.CODE)
  nodes_imgs = split_nodes_image(nodes_delimiter_bic)
  final_nodes = split_nodes_link(nodes_imgs)
  return final_nodes

def markdown_to_blocks(markdown):
  """
  Function used to parse a markdown document into multiple strings representing individual blocks

  Parameters
  -------
  markdown : str
    A markdown document
  
  Returns
  -------
  list:
    A list of non-empty text blocks
  """
  blocks = markdown.split('\n\n')
  # Use map to strip whitespace from every block in 'blocks', use the output of map to filter in only non-empty strings
  # finally parse the result to a list
  return list(filter(lambda y: len(y) > 0, map(lambda x: x.strip(), blocks)))

def block_to_block_type(block):
  """
    Function used to identify the type of content in a specific block

    Parameters
    -------
    block : str
      A block of markdown text
    
    Returns
    -------
    enum:
      The type of content in the block as defined by BlockType
  """
  if lines_startwith_pattern(block, r'[#]{1,6}[ ]'):
    return BlockType.HEADING
  elif block.startswith("```") and block.endswith("```"):
    return BlockType.CODE
  elif lines_startwith_pattern(block, r'>'):
    return BlockType.QUOTE
  elif lines_startwith_pattern(block, r'- '):
    return BlockType.UNORDERED_LIST
  elif lines_startwith_pattern(block, r'\d+[. ]'):
    return BlockType.ORDERED_LIST
  else:
    return BlockType.PARAGRAPH
  
def lines_startwith_pattern(block, pattern): 
  """
  Auxiliary function to generically check if every line in a markdown block starts with a particular pattern

  Parameters
  -------
  block : str
    A block of markdown text
  pattern: str
    The pattern to match

  Returns
  -------
  bool:
    True if every line in the block starts with the same pattern, False otherwise
  """
  block_lines = block.split('\n')
  result = True
  
  for line in block_lines:
    found = re.match(pattern, line)
    if not found:
      result = False
      break
  
  return result