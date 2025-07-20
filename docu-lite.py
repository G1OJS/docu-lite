"""
    This is a demo of docu-lite semi-automatic documentation, using this same
    file as the input test case. To try it on your own files,
    change these lines below:
        input_folder = ""
        output_name = "docu-lite-demo-outline.html"
        style_sheet = "docu-lite-style.css"
    Remember that if you use a path containing "\", you'll need to escape them by
    adding another "\" e.g. input_folder = "C:\\users\\me\\mydocs\\test.py"
"""
import html
import glob
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Generate an HTML doc outline from source code.")
    parser.add_argument("-i", "--input", nargs="*", default="./*.py",
                        help="Input filenames (default: ./*.py)")
    parser.add_argument("-o", "--output", default="docu-lite-outline.html",
                        help="Output HTML file (default: docu-lite-outline.html)")
    parser.add_argument("-s", "--style", default="docu-lite-style.css",
                        help="Output CSS file (default: docu-lite-style.css)")
    return parser.parse_args()

class docobj:
    """ structure to contain information about each object in the document """
    def __init__(self, signature):
        self.signature = signature.strip()
        self.object_type = self.signature.split(" ")[0]
        self.docstring =[]
        self.content_start = 0
        self.content_end = 0
        self.indent_spaces = len(signature) - len(signature.lstrip())
        self.indent_level = 0

def get_doc_objects(lines, object_signatures = ['class','def','docstring','body']):
        """
            document-level properties
            converts document into set of docobj in self.objects
            'docstring','text' represent the opening and closing docstring quotes 
        """
        objects = []
        indent_level = 0
        indent_spaces = 0

        # replace all opening docstring markers with 'docstring' and closing tags with 'body'
        opening_tag = True
        for line_no, line in enumerate(lines):
            if(line.strip() == '"""'):
                lines[line_no] = line.replace('"""','docstring' if opening_tag else 'body')
                opening_tag = not opening_tag
          
        # find and create document objects and tell them the line numbers
        # that their content starts and ends at
        for line_no, line in enumerate(lines):
            for p in object_signatures:
                if line.strip().startswith(p):
                    obj = docobj(line)
                    obj.content_start = line_no + 1         # start of this object
                    if(len(objects) > 0):           
                        objects[-1].content_end = (line_no) # end of previous object
                    objects.append(obj)
        objects[-1].content_end = len(lines)                # end of last object in document
               
        # tell the object what its indent level is within the document
        indents =[0]
        for obj in objects:
            if(obj.indent_spaces > indents[-1]):
                indents.append(obj.indent_spaces)
            obj.indent_level = indents.index(obj.indent_spaces)

        return objects

def object_list_to_HTML(lines, doc_objects):
    """
        converts list of doc_objects into HTML
    """
    doc_html = ""
    for i,obj in enumerate(doc_objects):
        nextobj = doc_objects[(i+1) % len(doc_objects)]
        details_open = ' open' if (obj.object_type == 'docstring') else ''
        doc_html += f"<details{details_open}><summary><span class ='{obj.object_type} {'signature'}'>{obj.signature}</span></summary>\n"
        if(nextobj.indent_level <= obj.indent_level):
            doc_html += f"<pre class ='{obj.object_type} content'>"
            for line in lines[obj.content_start:obj.content_end]:
                doc_html += f"{html.escape(line)}"
            doc_html += "</pre>\n"
            for i in range(obj.indent_level - nextobj.indent_level + 1):
                doc_html += "</details>\n"
    return doc_html
            
def main(input_pattern, style_sheet, output_name):
    """
        Another docstring for testing
    """
    output_html =  f"<!DOCTYPE html><html lang='en'>\n<head>\n<title>{output_name}</title>"
    output_html += f"<link rel='stylesheet' href='./{style_sheet}' />"
    output_html += "<body>\n"

    for filepath in glob.glob(input_pattern):
        filename = os.path.basename(filepath)
        print(f"Found file: {filename}")
        with open(filepath,"r") as f:
            lines = f.readlines()
        if(len(lines) ==0):
            print(f"File: {filename} has no content - skipping")
            continue
        output_html += f"<span class = 'filename'>{filename}</span><br>"
        doc_objects = get_doc_objects(lines)
        output_html += object_list_to_HTML(lines, doc_objects)
        
    output_html += "</body>\n"
    with open(output_name, "w", encoding="utf-8") as f:
        f.write(output_html)
    print(f"\n\nOutline written to {output_name}.html")

if __name__ == "__main__":
    args = parse_args()
    main(args.input, args.style, args.output)

