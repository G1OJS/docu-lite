"""
    This may be the most promising for very lightweight semi-automatic documentation
    + classes make it neat and readable
    + it works

    Next steps
        - ensure that 'firstline' handles multiline argument lists '(' to ')'
        - tidy up the html formatting
            - several functions for different layouts?
            - sort out indentation in body text
            - check if characters in main need escaping 
"""

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
        
            
def main():
    html =  "<!DOCTYPE html><html lang='en'><head><title>Code Outline</title>"
    html += "<style> * {font-weight:bold;padding-left:2rem;}"
    html += ".filename {padding-left:0em;}"
    html += ".docstring { font-weight:normal; color:green;}"
    html += ".docstring.text { font-weight:normal; color:green;}"
    html += ".class {color:blue;}"
    html += ".def {color:orange; }"
    html += ".text {color:black; font-size:1rem; font-weight:normal; }"
    html += "</style></head><body>"

    filepath = ""
    verbose = True
    for fname  in ["make_outline.py"]:
        html += f"<div class = 'filename'>{fname}</div>"
        doc = get_doc(filepath + fname, ['class','def','docstring','text'])
        for i,obj in enumerate(doc.objects):
            if(verbose):
                print(f"Level {obj.indent_level} object, firstline =  {obj.firstline}")
                for l in obj.lines:
                    print(f"{'    ' * obj.indent_level} {l.replace('\n','')}")
            nextobj = doc.objects[(i+1) % len(doc.objects)]
            if(nextobj.indent_level > obj.indent_level):
                html += f"<details><summary><span class ='{obj.html_class}'>{obj.firstline}</span></summary>"
            else:
                html += f"<details><summary><span class='{obj.html_class}'>{obj.firstline}</span></summary>"
                for line in obj.lines[1:]:
                    html += f"<div class ='{obj.html_class} text'>{line}</div>\n"
                html += "</details>"
            if(nextobj.indent_level < obj.indent_level):
                html += "</details>"
               
    outname = "outline.html"
    with open(outname, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n\nOutline written to {outname}")

if __name__ == "__main__":
    main()

