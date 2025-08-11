\# Code Language Statistics Analyzer



\[!\[Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/downloads/)

\[!\[License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



A simple yet powerful command-line tool to analyze your project's source code and report language statistics, similar to how GitHub displays repository language summaries.



It scans a directory, identifies file types, counts lines of code for each language, and presents the results in a beautiful, easy-to-read table right in your terminal.



\## Demo



The script uses the \[rich](https://github.com/Textualize/rich) library to generate beautiful, colorful output.



!\[Demo Screenshot](https://github.com/user-attachments/assets/23a73d8b-e120-4b45-99bb-05267183ec28)



\*If `rich` is not installed, it gracefully falls back to a clean plain-text table.\*



\## Features



\- \*\*Language Detection\*\*: Identifies programming languages based on file extensions.

\- \*\*Line \& File Counting\*\*: Counts the total number of files and lines of code for each language.

\- \*\*Percentage Analysis\*\*: Calculates the percentage contribution of each language to the total codebase.

\- \*\*`.gitignore` Support\*\*: Intelligently ignores files and directories specified in your `.gitignore` file with the `--gitignore` flag.

\- \*\*Beautiful Output\*\*: Displays results in a clean, colorful, and well-formatted table (requires `rich`).

\- \*\*Cross-Platform\*\*: Works on Windows, macOS, and Linux.

\- \*\*No Dependencies for Basic Use\*\*: Runs out-of-the-box for basic analysis. `rich` and `pathspec` are optional but recommended for the best experience.



\## Requirements



\- \*\*Python 3.7+\*\*



For the best experience, install the optional libraries:

\- `rich`: For beautiful, formatted table output.

\- `pathspec`: To enable `.gitignore` file handling.



You can install them easily using `pip`:

```bash

pip install rich pathspec

```



\## Usage



1\.  Clone this repository or download the `code\_stats.py` script.

2\.  Open your terminal and navigate to your project's directory.

3\.  Run the script.



\*\*Basic Usage (analyze current directory):\*\*

```bash

python code\_stats.py

```



\*\*Analyze a Specific Path:\*\*

```bash

python code\_stats.py /path/to/your/project

```



\*\*Respecting `.gitignore`:\*\*



To exclude files and directories listed in your `.gitignore` file, use the `--gitignore` flag. This is highly recommended for accurate results.

```bash

python code\_stats.py --gitignore

```



\*\*Getting Help:\*\*

```bash

python code\_stats.py --help

```



\## Customization



You can easily extend the script to recognize more languages. Simply edit the `LANGUAGE\_MAP` dictionary at the top of the `code\_stats.py` file and add new file extensions and their corresponding language names.



```python

\# In code\_stats.py

LANGUAGE\_MAP = {

&nbsp;   # ... existing languages

&nbsp;   '.your\_ext': 'YourCustomLanguage',

&nbsp;   '.another\_ext': 'AnotherLanguage',

}

```



\## License



This project is licensed under the MIT License - see the \[LICENSE](LICENSE) file for details.



---



\*Made with ❤️ by \[raricycms](https://github.com/raricycms)\*

