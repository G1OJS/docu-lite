"""
    This is a demo of docu-lite semi-automatic documentation, using this same
    file as the input test case. To try it on your own files,
    change these lines below:
        input_folder = ""
        input_filenames = ["docu-lite.py"]
        output_name = "docu-lite-demo-outline.html"
        output_style = "docu-lite-style.css"
    Remember that if you use a path containing "\", you'll need to escape them by
    adding another "\" e.g. input_folder = "C:\\users\\me\\mydocs\\test.py"

    This is the initial version with everything contained in one file.

    Future versions may grow to a library-based project with different HTML generators etc

"""
import html

class docobj:
    """ Bottom level document object containing only text and text-related properties """
    """ Note that this version does not process single line docstrings """
    """ Nor does it handle two
        line docstrings like this one """
    def __init__(self, signature):
        self.signature = signature.strip()
        self.html_class = self.signature.split(" ")[0]
        self.docstring =[]
        self.lines = []
        self.indent_spaces = len(signature) - len(signature.lstrip())
        self.indent_level = 0

class get_doc_objects:
    def __init__(self, filepath, object_types = ['class','def','docstring','body']):
        """
            document-level properties and file reader / preprocessor
            converts document into set of docobj in self.objects
            'docstring','text' represent the opening and closing docstring quotes 
        """
        self.objects = []
        indent_level = 0
        indent_spaces = 0
        # get input file into lines
        with open(filepath,"r") as f:
            lines = f.readlines()

        # process docstrings to a common format:
        #   ignore """text""" and """text\ntext""", otherwise:
        #    - replace all opening docstring markers with 'docstring'
        #    - replace all closing docstring makers with 'body'
        opening_tag = True
        for idx, line in enumerate(lines):
            if(line.strip() == '"""'):
                rep = 'docstring' if opening_tag else 'body'
                opening_tag = not opening_tag
                lines[idx] = line.replace('"""',rep)

        # find document objects and remember the line number they start at
        line_index = []
        for line_no, line in enumerate(lines):
            for p in object_types:
                if line.strip().startswith(p):
                    self.objects.append(docobj(line))
                    line_index.append(line_no)

        # fill the object.lines[] with the text within the object
        for obj_ind, obj_start_line_no in enumerate(line_index):
            obj = self.objects[obj_ind]
            last_line = line_index[obj_ind+1] if obj_ind < len(self.objects)-1 else len(lines)
            for obj_line_ind in range(obj_start_line_no, last_line):
                obj.lines.append(f"{lines[obj_line_ind]}")

        # tell the object what its indent level is within the document
        indents =[0]
        for obj in self.objects:
            if(obj.indent_spaces > indents[-1]):
                indents.append(obj.indent_spaces)
            obj.indent_level = indents.index(obj.indent_spaces)


def object_list_to_HTML(doc, verbose = False):
    """
        converts list of doc_objects into HTML
    """
    doc_html = ""
    for i,obj in enumerate(doc.objects):
        if(verbose):
            print(f"Level {obj.indent_level} object, signature =  {obj.signature}")
            for l in obj.lines:
                print(f"{'    ' * obj.indent_level} {l.replace('\n','')}")
        nextobj = doc.objects[(i+1) % len(doc.objects)]
        doc_html += f"<details><summary><span class ='{obj.html_class} {'signature'}'>{obj.signature}</span></summary>\n"
        if(nextobj.indent_level <= obj.indent_level):
            doc_html += f"<pre class ='{obj.html_class}'>"
            for line in obj.lines[1:]:
                doc_html += f"{html.escape(line)}"
            doc_html += "</pre>\n"
            for i in range(obj.indent_level - nextobj.indent_level + 1):
                doc_html += "</details>\n"
    return doc_html
            
def main():
    """
        Another docstring for testing
    """
    input_folder = ""
    input_filenames = ["docu-lite.py"]
    output_name = "docu-lite-demo-outline.html"
    output_style = "docu-lite-style.css"
    
    output_html =  f"<!DOCTYPE html><html lang='en'>\n<head>\n<title>{output_name}</title>"
    output_html += f"<link rel='stylesheet' href='./{output_style}' />"
    output_html += "<body>\n"

    for fname in input_filenames:
        output_html += f"<span class = 'filename'>{fname}</span><br>"
        doc_objects = get_doc_objects(input_folder + fname)
        output_html += object_list_to_HTML(doc_objects)

    output_html += "</body>\n"
 
    with open(output_name, "w", encoding="utf-8") as f:
        f.write(output_html)

    print(f"\n\nOutline written to {output_name}.html")

if __name__ == "__main__":
    main()

