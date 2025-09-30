import os
import shutil   
from textnode import TextNode, TextType
from utility import *

def main():
    print("Copying static to public...")
    recursive_copy("static", "public")
    print("Generating HTML pages...")
    generate_pages_recursive("content/", "template.html", "public/")


def recursive_copy(src="static/", dst="public/"):
    # Delete all content in the destination directory
    if os.path.exists(dst):
        print(f"Deleting existing content in {dst}...")
        shutil.rmtree(dst)
    print(f"Creating directory {dst}")
    os.makedirs(dst, exist_ok=True)

    # Recursively copy all content from src to dst
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            print(f"Recursive copy {s} to {d}...")
            recursive_copy(s, d)
        else:
            print(f"Copying file from {s} to {d}...")
            shutil.copy2(s, d)

main()