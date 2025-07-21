"""
    This is a demo of docu-lite semi-automatic documentation, using this same 
    file as the input test case. To try it on your own files,
    change the appropriate settings in docu-lite.ini
"""
import html
import glob
import os
import configparser
import argparse

def get_config():
    DEFAULT_INI = "[input] \npattern = ./*.py\n\n[output]\nhtml = docu-lite-outline.html\ncss = docu-lite-style.css\n\n[options]\ndocumentation_mode = off\nignore_docstrings_with = "
    DEFAULT_INI_FILE = "docu-lite.ini"

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--config", default = DEFAULT_INI_FILE)
    args, _ = parser.parse_known_args()
    path = args.config

    if not os.path.exists(path):
        if path != DEFAULT_INI_FILE:
            print(f"Config file not found: {path}. Is there a typo?")
            sys.exit(1)
        else:
            print(f"No config file found — creating default '{path}'")
            with open(path, "w") as f:
                f.write(DEFAULT_INI)

    print(f"Using config {path}")
    config = configparser.ConfigParser()
    config.read(path)
    return config

class docobj:
    """
        structure to contain information about each object in the document
    """
    def __init__(self, signature):
        self.signature = signature.strip()                              # first line of the object including the def, class etc
        self.indent_spaces = len(signature) - len(signature.lstrip())   # number of spaces up to first letter in signature line
        self.indent_level = 0                                           # indent level of this object
        self.object_type = self.signature.split(" ")[0]                 # see object_signatures=[] in get_doc_objects for possible values
        self.content_start = 0                                          # index of line file_lines one after first line of object
        self.content_end = 0                                            # index of line file_lines containing last line of object

def get_doc_objects(file_lines):
        """
            document-level properties
            converts document into set of docobj in self.objects
        """
        object_signatures = ['class','def','docstring','body']
        objects = []
        indent_level = 0
        indent_spaces = 0

        # replace all opening docstring markers with 'docstring' and closing tags with 'body'
        # so 'body' means otherwise unclassified content following a docstring
        # and in the example css is given the same style as unclassified content following def and class
        docstring_tag_is_opener = False
        for line_no, line in enumerate(file_lines):

            if(line.strip().startswith('"""')):         # 3quotes starting a line or alone
                docstring_tag_is_opener = not docstring_tag_is_opener
                if(line.strip().replace('"""','',1).endswith('"""')):       # 3quotes ending a line that starts with 3quotes
                    docstring_tag_is_opener = False
            elif(line.strip().endswith('"""')):         # 3quotes ending a line that doesn't start with 3quotes
                docstring_tag_is_opener = False

            if('"""' in line):                          # 3quotes anywhere in line
                if docstring_tag_is_opener:
                    file_lines[line_no] = line.replace('"""','docstring ',1)
                else:
                    file_lines[line_no] = line.replace('"""',' body ',1)
        

            
        # find and create document objects and tell them the line numbers
        # that their content starts and ends at
        for line_no, line in enumerate(file_lines):
            for p in object_signatures:
                if line.strip().startswith(p):
                    obj = docobj(line)
                    obj.content_start = line_no + 1         # start of this object
                    if(len(objects) > 0):           
                        objects[-1].content_end = (line_no) # end of previous object
                    objects.append(obj)
        if(len(objects)>1):
            objects[-1].content_end = len(file_lines)            # end of last object in document

        # tell the object what its indent level is within the document
        indents =[0]
        for obj in objects:
            if(obj.indent_spaces > indents[-1]):
                indents.append(obj.indent_spaces)
            obj.indent_level = indents.index(obj.indent_spaces)
        return objects


def _ignore_docstrings_with(doc_objects, file_lines, pattern):
    for obj in doc_objects:
        if (not obj.object_type == 'docstring'):
            continue
        text = file_lines[obj.content_start: obj.content_end]
        text = ''.join(text)
        if (pattern in text):
            obj.object_type = 'ignore'
    return doc_objects


def _signature_html(obj_type, obj_signature, open_details = True):
    # write the signature of the object with a summary / details tag
    htm = "<details><summary>" if open_details else "<div>"
    htm += f"<span class ='{obj_type} {'signature'}'>{obj_signature}</span>"
    htm += "</summary>" if open_details else "</div>"
    return htm + "\n"

def _content_html(file_lines, object_type, start_no, end_no):
    # write 'content' inside <pre></pre>
    htm = f"<pre class ='{object_type} content'>"
    if(object_type == 'docstring'):
        htm += file_lines[start_no-1].replace('docstring','',1)  # 3quotes followed immediately by text
    for line in file_lines[start_no:end_no]:
        htm += f"{html.escape(line)}"
    htm += "</pre>\n"
    return htm

def _close_details(n_times):
    return "</details>\n" * n_times

def object_list_to_HTML(file_lines, doc_objects):
    """
        converts list of doc_objects into HTML
    """
    doc_html = ""
    for i,obj in enumerate(doc_objects):
        nextobj = doc_objects[(i+1) % len(doc_objects)]
        if(obj.object_type == 'ignore'):
            continue
        
        doc_html += _signature_html(obj.object_type, obj.signature, open_details = True)
        if(nextobj.indent_level <= obj.indent_level):
            doc_html += _content_html(file_lines, obj.object_type, obj.content_start, obj.content_end)
            doc_html += _close_details(obj.indent_level - nextobj.indent_level + 1)
            
    return doc_html

def object_list_to_documentation_HTML(file_lines, doc_objects):
    """
        converts list of doc_objects into HTML
    """
    doc_html = ""
    for i,obj in enumerate(doc_objects):
        nextobj = doc_objects[(i+1) % len(doc_objects)]
        if(obj.object_type == 'ignore'):
            continue    
        
        if(obj.object_type not in ['body','docstring']):
            doc_html += "<hr>"
            doc_html += _signature_html(obj.object_type, obj.signature.replace('def ','&nbsp&nbsp&nbsp'), open_details = False)
        if(obj.object_type == "docstring"):
            doc_html += _content_html(file_lines, obj.object_type, obj.content_start, obj.content_end)

    return doc_html
            
def main():
    """
        Another docstring for testing
    """
    version_string = "v0.8.0"
    soft_string = f"Docu-lite {version_string} by Alan Robinson: github.com/G1OJS/docu-lite/"
    print(f"{soft_string}\n")
    config = get_config()
    input_pattern = config.get("input", "pattern")
    output_name = config.get("output", "html")
    style_sheet = config.get("output", "css")
    documentation_mode = config.get("options", "documentation_mode")
    ignore_docstrings_with = config.get("options", "ignore_docstrings_with")

    print(f"Running with \n \n[input]\npattern = {input_pattern}\n[output]\nhtml = {output_name}\ncss = {style_sheet}\ndocumentation_mode = {documentation_mode}\n")
    
    # start the output html
    output_html =  f"<!DOCTYPE html><html lang='en'>\n<head>\n<title>{output_name}</title>"

    # look for specified or default css, if not found write a new one and use that
    DEFAULT_CSS = "* {margin-left:2rem;} \n.filename {font-weight:bold; color:grey; font-size:2rem;} \
        \n.signature {font-weight:bold; margin-left:2rem;}\n.class {color:blue;} \
        \n.def {color:orange; }\n.docstring {color:darkgreen;}\n \
        \n.content {border-left: 2px solid #ccc; color:black; padding-left: 1em; background: #f9f9f9;}\n.docstring {color:green;}"

    DEFAULT_CSS_DOCS = "* {margin-left:2rem; background: #e6f9ff;} \n.filename {font-weight:bold; color:grey; font-size:2rem;} \
        \n.signature {font-weight:bold; margin-left:2rem;}\n.class {color:black; font-size:1.5rem;} \
        \n.def {color:black; }\n.docstring {color:darkgreen;}\n \
        \n.content {color:black; padding-left: 1em; }\n.docstring {color:green;}"

    try:
        with open(style_sheet, "r", encoding="utf-8") as f:
            pass
    except (FileNotFoundError, OSError):
        print(f"Couldn't open style sheet {style_sheet}: creating default\n")
        with open(style_sheet, "w", encoding="utf-8") as f:
            f.write(DEFAULT_CSS if (documentation_mode=="off") else DEFAULT_CSS_DOCS)
    output_html += f"<link rel='stylesheet' href='./{style_sheet}' />"

    # start html body and process input files
    output_html += "<body>\n"
    print(f"Scanning for input files in {input_pattern}")
    for filepath in glob.glob(input_pattern):
        filename = os.path.basename(filepath)
        print(f"Found file: {filename}")
        with open(filepath,"r") as f:
            file_lines = f.readlines()
        if(len(file_lines) ==0):
            print(f"File: {filename} has no content - skipping")
            continue

        doc_objects = get_doc_objects(file_lines)
        if(ignore_docstrings_with != ''):
            print(f"Ignoring docstrings containing {ignore_docstrings_with}")
            doc_objects =  _ignore_docstrings_with(doc_objects, file_lines, ignore_docstrings_with)

        output_html += f"<span class = 'filename'>{filename}</span><br>"
        if(documentation_mode == "off"):
            output_html += object_list_to_HTML(file_lines, doc_objects)
        else:
            output_html += object_list_to_documentation_HTML(file_lines, doc_objects)

    # write footer
    output_html += f"\n<br><br><span style = 'font-size:0.8em;color:#666;border-top:1px solid #ddd; "
    output_html += f"font-style:italic'>Made with {soft_string}</span>"

    # close html body and write the file
    output_html += "</body>\n"
    with open(output_name, "w", encoding="utf-8") as f:
        f.write(output_html)
    print(f"\nOutline written to {output_name},")
    print(f"linking to style sheet {style_sheet}")

if __name__ == "__main__":
    main()

