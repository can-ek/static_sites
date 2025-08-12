from textnode import *
from htmlnode import HTMLNode
from leafnode import LeafNode
from markdownprocess import generate_page
from sys import argv
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
  public_path = './docs'
  static_path = './static'
  if os.path.exists(public_path) and os.path.isdir(public_path):
    shutil.rmtree(public_path, True)
    os.mkdir(public_path)
    print(f'Removed contents and created path for {public_path}')
  copy_dir(static_path, public_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
  print(f'Reading contents in {dir_path_content}')
  contents = os.listdir(dir_path_content)
  for sub_path in contents:
    new_src = os.path.join(dir_path_content, sub_path)
    if os.path.isdir(new_src):
      new_dest = os.path.join(dest_dir_path, sub_path)
      os.mkdir(new_dest)
      print(f'Created new directory {new_dest}')
      generate_pages_recursive(new_src, template_path, new_dest, base_path)
    else:
      new_dest = os.path.join(dest_dir_path, 'index.html')
      generate_page(new_src, template_path, new_dest, base_path)
      print(f'Generated new page from {new_src} to {new_dest}')

def main():
  if len(argv) == 2:
    base_path = argv[1]
  else:
    base_path = '/'

  copy_to_public()
  generate_pages_recursive('./content', './template.html', './docs', base_path)

main()
