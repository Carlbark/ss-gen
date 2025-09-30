import os
import shutil   
import sys
from textnode import TextNode, TextType
from utility import *

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f"Basepath set to: {basepath}")
    print("Copying static to docs...")
    recursive_copy("static", "docs")
    print("Generating HTML pages...")
    generate_pages_recursive("content/", "template.html", "docs/", basepath)


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