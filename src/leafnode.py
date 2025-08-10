from htmlnode import HTMLNode

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props = None):
    """
    Parameters
    -------
    tag : str
      The HTML tag this node represents
    value : str
      The text value in the HTML tag
    props: dict, optional
      Properties to apply to the tag    
    """
    super().__init__(tag, value, None, props)

  def to_html(self):
    """
    Transform the object into its HTML representation

    Returns
    -------
    str
      An HTML string representation of the node or the raw text in
      'value' if no 'tag' is present
    
    Raises
    -------
    ValueError
      If the node doesn't have a value
    """
    if not self.value:
      raise ValueError("Missing value")
    if not self.tag:
      return self.value
    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"