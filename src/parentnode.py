from htmlnode import HTMLNode

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)

  def to_html(self):
    if self.tag is None:
      raise ValueError("Parent node must have a tag")
    if self.children is None or len(self.children) == 0:
      raise ValueError("Parent must have children")
    
    result = f"<{self.tag}{self.props_to_html()}>"
    for node in self.children:
      result += node.to_html()
    result += f"</{self.tag}>"
    return result