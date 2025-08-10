from textnode import *
from htmlnode import HTMLNode
from leafnode import LeafNode
import shutil
import os

def copy_dir(src_path, dest_path):
  print(f'Reading files in dir {src_path}')
  contents = os.listdir(src_path)
  for sub_path in contents:
    new_src = os.path.join(src_path, sub_path)
    new_dest = os.path.join(dest_path, sub_path)
    if os.path.isdir(new_src):
      os.mkdir(new_dest)
      print(f'Created new directory {new_dest}')
      copy_dir(new_src, new_dest)
    else:
      shutil.copy(new_src, new_dest)
      print(f'Copied contents from {new_src} to {new_dest}')

def copy_to_public():
  public_path = './public'
  static_path = './static'
  if os.path.exists(public_path) and os.path.isdir(public_path):
    shutil.rmtree(public_path, True)
    os.mkdir(public_path)
    print(f'Removed contents and created path for {public_path}')
  copy_dir(static_path, public_path)

  

def main():
  node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
  print(node)

  html_node = HTMLNode('p', 'paragraph', [], {"href": "https://www.google.com", "target": "_blank"})
  print(html_node)

  print(LeafNode("p", "This is a paragraph of text.").to_html())
  copy_to_public()

main()
