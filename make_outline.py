"""
    This may be the most promising for very lightweight semi-automatic documentation
    + classes make it neat and readable
    + it works

    Next steps
        - ensure that 'firstline' handles multiline argument lists '(' to ')'
        - tidy up the doc_html formatting
            - several functions for different layouts?
            - sort out indentation in body text
"""
import html

class docobj:
    """ Bottom level document object containing only text and text-related properties"""
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
        # replace all opening docstring markers with 'docstring'
        # replace all closing docstring makers with 'text'
        opening = True
        for idx, line in enumerate(lines):
            if(('"""' in line) and not ('"""' in line.replace('"""','',1))):
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
    doc_html =  "<!DOCTYPE doc_html><doc_html lang='en'><head><title>Code Outline</title>"
    doc_html += "<style> * {font-weight:bold;padding-left:2rem;}"
    doc_html += ".filename {padding-left:0em;}"
    doc_html += ".docstring { font-weight:normal; color:green;}"
    doc_html += ".docstring.text { font-weight:normal; color:green;}"
    doc_html += ".class {color:blue;}"
    doc_html += ".def {color:orange; }"
    doc_html += ".text {color:black; font-size:1rem; font-weight:normal; }"
    doc_html += "</style></head><body>"
    return doc_html

def doc_body(doc, verbose = False):
    doc_html = ""
    for i,obj in enumerate(doc.objects):
        if(verbose):
            print(f"Level {obj.indent_level} object, firstline =  {obj.firstline}")
            for l in obj.lines:
                print(f"{'    ' * obj.indent_level} {l.replace('\n','')}")
        nextobj = doc.objects[(i+1) % len(doc.objects)]
        if(nextobj.indent_level > obj.indent_level):
            doc_html += f"<details><summary><span class ='{obj.html_class}'>{obj.firstline}</span></summary>"
        else:
            doc_html += f"<details><summary><span class='{obj.html_class}'>{obj.firstline}</span></summary>"
            for line in obj.lines[1:]:
                doc_html += f"<div class ='{obj.html_class} text'>{html.escape(line).replace(' ','&nbsp')}</div>\n"
            doc_html += "</details>"
        if(nextobj.indent_level < obj.indent_level):
            for i in range(obj.indent_level - nextobj.indent_level):
                doc_html += "</details>"
    return doc_html
            
def main():
    doc_html = html_head()

    filepath = ""
    verbose = True
    for fname  in ["make_outline.py"]:
        doc_html += f"<div class = 'filename'>{fname}</div>"
        doc = get_doc(filepath + fname, ['class','def','docstring','text'])
        doc_html += doc_body(doc, verbose = True)

    outname = "outline.html"
    with open(outname, "w", encoding="utf-8") as f:
        f.write(doc_html)

    print(f"\n\nOutline written to {outname}")

if __name__ == "__main__":
    main()

