class HTMLNode:
  def __init__(self, tag = None, value = None, children = None, props = None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props
  
  def to_html(self):
    raise NotImplementedError()
  
  def props_to_html(self):
    html = ""

    if self.props:
      for k,v in self.props.items():
        html += f" {k}=\"{v}\""
    return html
  
  def __repr__(self):
    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}> children: { 0 if self.children == None else len(self.children)}"