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
docu-lite -i /folder/*.py -s style.css -o outline.html
```

