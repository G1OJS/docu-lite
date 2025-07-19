"""
    This may be the most promising for very lightweight semi-automatic documentation
    + classes make it neat and readable
    + it works

    The issue with previous versions was trying to nest defs within classes for not much gain

    Next steps
      - tidy up the html formatting
        - remove the word 'def'?
        - ensure that 'firstline' handles multiline argument lists ( to )
        - code to extract the class __init__() too?
      - write down the 'rules' e.g. only one docstring right at the top of class and def
        
"""



class docobj:
    def __init__(self, firstline):
        self.firstline = firstline.strip()
        self.html_class = self.firstline.split(" ")[0]
        self.docstring =[]
        self.text = []
        self.indent_spaces = len(firstline) - len(firstline.lstrip())
        self.indent_level = 0
        
    def isolate_docstring(self):
        in_multiline_docstring = False
        to_remove = []
        for idx, line in enumerate(self.text):
            if('"""' in line):
                if(in_multiline_docstring):
                    break
                else:
                    in_multiline_docstring = True
            if(in_multiline_docstring):
                self.docstring.append(line)
                to_remove.append(idx)
        for idx in reversed(to_remove):
            del self.text[idx]

class get_doc:
    def __init__(self,filepath):
        self.objects = []
        obj = None
        indent_level = 0
        indent_spaces = 0
        with open(filepath,"r") as f:
            lines = f.readlines()
        for line in lines:
            for p in ['class','def']:
                if line.strip().startswith(p):
                    if(obj is not None):
                        self.objects.append(obj)
                    obj = docobj(line)
            if (obj is not None):
                obj.text.append(line)

        for obj in self.objects:
            obj.isolate_docstring()
            if(obj.indent_spaces > indent_spaces):
                indent_level +=1
            if(obj.indent_spaces < indent_spaces):
                indent_level -=1
            indent_spaces = obj.indent_spaces
            obj.indent_level = indent_level
            

def main():
    html =  "<!DOCTYPE html><html lang='en'><head><title>Code Outline</title>"
    html += "<style> * {font-weight:bold;padding-left:2em;}"
    html += ".filename {padding-left:0em;}"
    html += ".docstring {margin-left:2em; font-weight:normal; color:green;}"
    html += ".class {color:blue;}"
    html += ".def {color:orange; }"
    html += "</style></head><body>"

    filepath = "C:\\Users\\drala\\Documents\\Projects\\GitHub\\NECBOL\\necbol\\"
    for fname  in ["modeller.py","gui.py","components.py","optimisers.py"]:
        html += f"<div class = 'filename'>{fname}</div>"
        doc = get_doc(filepath + fname)
        for obj in doc.objects:
            indent_str = "    " * obj.indent_level
            print(indent_str, obj.firstline)
                
    outname = "outline.html"
    with open(outname, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Outline written to {outname}")

if __name__ == "__main__":
    main()

