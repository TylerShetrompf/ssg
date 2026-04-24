from textnode import TextNode,TextType
import os
import shutil
from blocktohtml import markdown_to_html_node
import sys


def dir_cont_copy():

    if os.path.exists("./static") and os.path.exists("./docs"):
        
        shutil.rmtree("./docs")
        shutil.copytree("./static", "./docs")

    else:
        raise Exception("Missing static or docs folder")

def extract_title(markdown):

    lines = markdown.splitlines()

    if lines[0][:1] != "#":
        raise Exception("No h1 header")
    else:
        header = lines[0]
        header = header[1:]
        header = header.strip()
        return header

def generate_page(from_path, template_path, dest_path, basepath):

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
    cont = cont.replace('href="/', f'href="{basepath}')
    cont = cont.replace('src="/', f'src="{basepath}')


    new_file = open(dest_path, 'w')
    new_file.write(cont)
    new_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    
    list = os.listdir(dir_path_content)

    for item in list:
        
        item_path = os.path.join(dir_path_content, item)
        
        dest_path = os.path.join(dest_dir_path, item)
        
        if os.path.isdir(item_path):
            
            if not os.path.isdir(dest_path):
                os.mkdir(dest_path)
    
            generate_pages_recursive(item_path, template_path, dest_path, basepath)
        
        else:

            if item[-3:] == ".md":
                
                html_path = dest_path[:-3] + ".html"
                generate_page(item_path, template_path, html_path, basepath)

# test case
def main():

    basepath = ""

    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    
    dir_cont_copy()
    generate_pages_recursive("./content/", "./template.html", "./docs/", basepath)
    #generate_page("./content/index.md", "./template.html", "./public/index.html")

main()