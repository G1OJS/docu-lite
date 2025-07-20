# 🧾 docu-lite [![PyPI Downloads](https://static.pepy.tech/badge/docu-lite)](https://pepy.tech/projects/docu-lite)
### Ultra-light Zero-dependency HTML outline generator for Python.  



* Browse classes and functions with collapsible docstrings in a tidy, readable format.
* Specify your own stylesheet(s) or rely on the default (will be generated on run)
* Ultra-light: no dependencies, short script
* [Integrate into your GitHub Workflow](https://g1ojs.github.io/docu-lite/add-to-workflow/) for Up to Date outline in your repo
* Produces output like this:
    - [live file](https://g1ojs.github.io/docu-lite/docu-lite-outline.html)
    - [live file - documentation mode](https://g1ojs.github.io/docu-lite/docu-lite-outline_docs.html)
    - screenshot below

![Capture](https://github.com/user-attachments/assets/c2eb5243-5666-428a-a1f7-4a09ec127285)

## 🛠 Installation

Install using pip: open a command window and type

```
pip install docu-lite
```
## Usage
Either edit and run docu-lite.py in an IDE, or run from the command line:
```
docu-lite [-i INPUT_PATTERN] [-o OUTPUT_FILE] [-s CSS_FILE] [--documentation]
```
Arguments:

-i specifies the input file pattern, e.g. /folder/folder/*.py

-o specifies the name for the output file e.g. /folder/folder/outline.html

-s specifies the name of the css file you want to use

--documentation produces less detailed output differently styled for use as, or editing to produce, documentation.
This mode uses a completely separate style sheet so can be tailored independently. Run docu-lite twice with and
without this option to produce two sets of output for different purposes.

*if you specify a css file, all docu-lite does is ensure that the output html references that file instead of the default

*if the default css file is missing, it will be generated and used


