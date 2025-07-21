# 🧾 docu-lite [![PyPI Downloads](https://static.pepy.tech/badge/docu-lite)](https://pepy.tech/projects/docu-lite) 
### ⚡ Ultra-light Zero-dependency HTML outline generator for Python.   



* 📖 Browse classes and functions with collapsible docstrings in a tidy, readable format.
* 📘 Specify your own stylesheet(s) or rely on the default (will be generated on run)
* ⚖️ Ultra-light: no dependencies, short script
* ⚙️[Integrate into your GitHub Workflow](https://g1ojs.github.io/docu-lite/add-to-workflow/) for Up to Date outline in your repo
* 👀 Produces output like this:
    - [live file](https://g1ojs.github.io/docu-lite/docu-lite-outline.html)
    - [live file - documentation mode](https://g1ojs.github.io/docu-lite/docu-lite-outline_docs.html)
    - screenshot below

![Capture](https://github.com/user-attachments/assets/c2eb5243-5666-428a-a1f7-4a09ec127285)

## 🛠 Installation

Install using pip: open a command window and type

```
pip install docu-lite
```
## 💡 Usage
Either edit and run docu-lite.py in an IDE, or run from the command line:
```
docu-lite
```
A config file 'docu-lite.ini' will be created in the current directory:
```
[input]
pattern = ./*.py

[output]
html = docu-lite-outline.html
css = docu-lite-style.css
documentation_mode = off
```
⚙️ Edit the config file to control how docu-lite runs:
 - Input **pattern** specifies where to look for input
 - **html** specifies the name of the output html file
 - **css** specifies the name of the input style sheet, which will be referenced from the output html file
 - **documentation_mode** produces a less detailed output styled for use as or editing into documentation. This mode uses a **completely separate stylesheet**, which can be tailored independently.  

📝 If the specified css file is not found, docu-lite will generate one and reference it in the html

[PyPI link](https://pypi.org/project/docu-lite/)
