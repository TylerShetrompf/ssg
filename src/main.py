from textnode import TextNode,TextType
import os
import shutil
from blocktohtml import markdown_to_html_node


def dir_cont_copy():

    if os.path.exists("./static") and os.path.exists("./public"):
        
        shutil.rmtree("./public")
        shutil.copytree("./static", "./public")

    else:
        raise Exception("Missing static or public folder")

def extract_title(markdown):

    lines = markdown.splitlines()

    if lines[0][:1] != "#":
        raise Exception("No h1 header")
    else:
        header = lines[0]
        header = header[1:]
        header = header.strip()
        return header

def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_file = open(from_path, 'r')
    from_contents = from_file.read()
    from_file.close()

    temp_file = open(template_path, 'r')
    temp_contents = temp_file.read()
    temp_file.close()

    html_node = markdown_to_html_node(from_contents)
    html_text = html_node.to_html()


    title = extract_title(from_contents)

    cont = temp_contents.replace(r"{{ Title }}", title)
    cont = cont.replace(r"{{ Content }}", html_text)

    new_file = open(dest_path, 'w')
    new_file.write(cont)
    new_file.close()

# test case
def main():
    dir_cont_copy()
    generate_page("./content/index.md", "./template.html", "./public/index.html")

main()