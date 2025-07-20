# 🧾 docu-lite
### Ultra-light Zero-dependency HTML outline generator for Python.  
* Browse classes and functions with collapsible docstrings in a tidy, readable format.
* Specify your own stylesheet(s)

Coming soon:
* Create simultaneous copies of HTML output from one source for different purposes / audiences
* Integrate into GitHub workflow so the outline is always up to date

Ultra-light: Just 100 lines to make HTML like this:

![Capture](https://github.com/user-attachments/assets/c2eb5243-5666-428a-a1f7-4a09ec127285)

## 🛠 Installation

Install using pip: open a command window and type

```
pip install docu-lite
```
## Usage
Either edit and run docu-lite.py in an IDE, or run from the command line:
```
docu-lite [-i INPUT_PATTERN] [-s CSS_FILE] [-o OUTPUT_FILE] [--include-css]
```
Arguments:
-i specifies the input file pattern, e.g. /folder/folder/*.py
-s specifies the name of the css file (should be in the folder that docu-lite is run from)
-o specifies the name for the output file e.g. /folder/folder/outline.html
--include-css tells docu-lite to copy the css file contents into the html, 
  so that the html file is self-contained (portable)

