import re
from textnode import TextType, TextNode
from parentnode import ParentNode
from blocktype import BlockType

#region Private
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

def block_type_to_tag(block_type):
  match(block_type):
    case BlockType.PARAGRAPH:
      return 'p'
    case BlockType.HEADING:
      return 'header'
    case BlockType.CODE:
      return 'code'
    case BlockType.QUOTE:
      return 'blockquote'
    case BlockType.UNORDERED_LIST:
      return 'ul'
    case BlockType.ORDERED_LIST:
      return 'ol'
    case _:
      raise ValueError('Invalid BlockType value')

def text_to_children(block):
  text_nodes = text_to_textnodes(block)
  html_nodes = []

  for node in text_nodes:
    html_nodes.append(node.to_html_node())
  return html_nodes

def block_to_html(block, block_type):
  html_nodes = text_to_children(block)
  tag = block_type_to_tag(block_type)
  return ParentNode(tag, html_nodes)    

#endregion

def extract_markdown_images(text):
  pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(pattern, text)
  return matches

def extract_markdown_links(text):
  pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(pattern, text)
  return matches

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
  lines = text.split("\n")
  paragraph = " ".join(lines)
  initial_node = TextNode(paragraph, TextType.NORMAL)
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

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node.to_html_node()
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.NORMAL)
    child = raw_text_node.to_html_node()
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)