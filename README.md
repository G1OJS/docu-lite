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
docu-lite [-i INPUT_PATTERN] [-o OUTPUT_FILE] [-s CSS_FILE] [--documentation]
```
### ⚙️ Arguments

- `-i`  
  **Input file pattern**, e.g.:  
  ```
  -i /folder/folder/*.py
  ```

- `-o`  
  **Output file name**, e.g.:  
  ```
  -o /folder/folder/outline.html
  ```

- `-s`  
  **CSS file to use**, e.g.:  
  ```
  -s /path/to/custom.css
  ```

- `--documentation`  
  Produces a less detailed output styled for use as or editing into documentation.  
  This mode uses a **completely separate stylesheet**, which can be tailored independently.  
  You can run `docu-lite` twice (with and without this flag) to generate two different outputs for different purposes.

---

### 📝 Notes

- If you specify a CSS file, **docu-lite simply references it** in the output HTML — it doesn't modify or generate it.
- If the default CSS file is missing, **it will be automatically generated** and used.

[PyPI link](https://pypi.org/project/docu-lite/)
