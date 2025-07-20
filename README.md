# 🧾 docu-lite
### Ultra-light Zero-dependency HTML outline generator for Python.  
* Browse classes and functions with collapsible docstrings in a tidy, readable format.
* Specify your own stylesheet(s) or rely on the default (will be generated on run)
* Ultra-light: no dependencies, short script
* [Integrate into your GitHub Workflow](https://github.com/G1OJS/docu-lite/blob/main/adding-to-GitHub-workflow.md) for Up to Date outline in your repo
* Produces output like this [live file](https://g1ojs.github.io/docu-lite/docu-lite-outline.html) and this:

![Capture](https://github.com/user-attachments/assets/c2eb5243-5666-428a-a1f7-4a09ec127285)

## 🛠 Installation

Install using pip: open a command window and type

```
pip install docu-lite
```
## Usage
Either edit and run docu-lite.py in an IDE, or run from the command line:
```
docu-lite [-i INPUT_PATTERN] [-o OUTPUT_FILE] [-s CSS_FILE] 
```
Arguments:

-i specifies the input file pattern, e.g. /folder/folder/*.py

-o specifies the name for the output file e.g. /folder/folder/outline.html

-s specifies the name of the css file you want to use

*if you specify a css file, all docu-lite does is ensure that the output html references that file instead of the default

*if the default css file is missing, it will be generated and used


