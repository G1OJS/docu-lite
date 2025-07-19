
            
            
def main():
    html =  "<!DOCTYPE html><html lang='en'><head><title>Code Outline</title>"
    html += "<style> * {font-weight:bold;padding-left:2rem;}"
    html += ".filename {padding-left:0em;}"
    html += ".docstring {margin-left:2em; font-weight:normal; color:green;}"
    html += ".class {color:blue;}"
    html += ".def {color:orange; }"
    html += ".text {color:black; font-size:1rem; font-weight:normal; }"
    html += "</style></head><body>"

    filepath = ""
    verbose = True
    for fname  in ["test.py"]:
        html += f"<div class = 'filename'>{fname}</div>"
        doc = get_doc(filepath + fname, ['main', 'class','def','"""'])
        for i,obj in enumerate(doc.objects):
            if(verbose):
                for l in obj.lines:
                    print("    " * obj.indent_level, l)
            nextobj = doc.objects[(i+1) % len(doc.objects)]
            if(nextobj.indent_level > obj.indent_level):
                html += f"<details><summary><span class ='{obj.html_class}'>{obj.firstline}</span></summary>"
            else:
                html += f"<div class ='{obj.html_class}'>{obj.firstline}</div>\n"
                html += "<details><summary>text</summary>"
                for line in obj.lines[1:]:
                    html += f"<div class ='{obj.html_class} text'>{line}</div>\n"
                html += "</details>"
            if(nextobj.indent_level < obj.indent_level):
                html += "</details>"
               
    outname = "outline.html"
    with open(outname, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n\nOutline written to {outname}")


