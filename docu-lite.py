"""
    This is a demo of docu-lite semi-automatic documentation, using this same
    file as the input test case. To try it on your own files,
    change these lines below:
        filepath = ""
        for fname  in ["docu-lite.py"]:
    Remember that if you use a path containing "\", you'll need to escape them by
    adding another "\" e.g. filepath = "C:\\users\\me\\mydocs\\test.py"

    This is the initial version with everything contained in one file.

    Future versions may grow to a library-based project with different HTML generators etc

"""
import html

class docobj:
    """ Bottom level document object containing only text and text-related properties """
    """ Note that this version does not process single line docstrings """
    """ Nor does it handle two
        line docstrings like this one """
    def __init__(self, firstline):
        self.firstline = firstline.strip()
        self.html_class = self.firstline.split(" ")[0]
        self.docstring =[]
        self.lines = []
        self.indent_spaces = len(firstline) - len(firstline.lstrip())
        self.indent_level = 0

class get_doc:
    def __init__(self,filepath, objtypes):
        """
            document-level properties and file reader / preprocessor
            completes with self.objects containing parsed docobjects
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
        #    - replace all closing docstring makers with 'text'
        opening = True
        for idx, line in enumerate(lines):
            if(line.strip() == '"""'):
                rep = 'docstring' if opening else 'text'
                opening = not opening
                lines[idx] = line.replace('"""',rep)

        # find document objects and remember the line number they start at
        line_index = []
        for line_no, line in enumerate(lines):
            for p in objtypes:
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


def html_head():
    doc_html =  "<!DOCTYPE doc_html><doc_html lang='en'>\n<head>\n<title>Code Outline</title>"
    doc_html += "<style>\n * {font-weight:bold;padding-left:2rem;}\n"
    doc_html += ".filename {padding-left:0em;}\n"
    doc_html += ".class {color:blue;}\n"
    doc_html += ".def {color:orange; }\n"
    doc_html += ".docstring {color:green;}\n"
    doc_html += ".text {color:black;}\n"
    doc_html += ".inner {font-size:1rem; font-weight:normal; white-space: pre;}\n"
    doc_html += ".def.inner {color:black;}\n"
    doc_html += ".class.inner {color:black;}\n"
    doc_html += "</style>\n</head>\n"
    return doc_html

def doc_body(doc, verbose = False):
    doc_html = ""
    for i,obj in enumerate(doc.objects):
        if(verbose):
            print(f"Level {obj.indent_level} object, firstline =  {obj.firstline}")
            for l in obj.lines:
                print(f"{'    ' * obj.indent_level} {l.replace('\n','')}")
        nextobj = doc.objects[(i+1) % len(doc.objects)]
        doc_html += f"<details><summary><span class ='{obj.html_class}'>{obj.firstline}</span></summary>\n"
        if(nextobj.indent_level <= obj.indent_level):
            for line in obj.lines[1:]:
                doc_html += f"<span class ='{obj.html_class} inner'>{html.escape(line)}</span>\n"
            for i in range(obj.indent_level - nextobj.indent_level + 1):
                doc_html += "</details>\n"
    return doc_html
            
def main():
    """
        Another docstring for testing
    """
    doc_html = html_head()
    doc_html += "<body>\n"

    filepath = ""
    for fname  in ["docu-lite.py"]:
        doc_html += f"<div class = 'filename'>{fname}</div>"
        doc = get_doc(filepath + fname, ['class','def','docstring','text'])
        doc_html += doc_body(doc, verbose = False)

    doc_html += "</body>\n"
    outname = "outline.html"
    with open(outname, "w", encoding="utf-8") as f:
        f.write(doc_html)

    print(f"\n\nOutline written to {outname}")

if __name__ == "__main__":
    main()

