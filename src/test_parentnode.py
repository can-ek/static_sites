import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
  def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

  def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

  def test_to_html_with_props(self):
    child_node = LeafNode("span", "child", {'padding': 'left'})
    parent_node = ParentNode("div", [child_node], {'align': 'center'})
    self.assertEqual(
        parent_node.to_html(),
        "<div align=\"center\"><span padding=\"left\">child</span></div>",
    )

  def test_to_html_without_children(self):
    parent_node = ParentNode("div", None)
    with self.assertRaises(ValueError) as cm1:
      parent_node.to_html()

    self.assertEqual(type(cm1.exception), ValueError)
    self.assertEqual(cm1.exception.args[0], 'Parent must have children')
    
    parent_node2 = ParentNode("div", [])
    with self.assertRaises(ValueError) as cm2:
      parent_node.to_html()

    self.assertEqual(type(cm2.exception), ValueError)
    self.assertEqual(cm2.exception.args[0], 'Parent must have children')

  def test_to_html_without_tag(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode(None, [child_node])
    
    with self.assertRaises(ValueError) as cm:
      parent_node.to_html()
    
    self.assertEqual(type(cm.exception), ValueError)
    self.assertEqual(cm.exception.args[0], 'Parent node must have a tag')

if __name__ == "__main__":
  unittest.main()