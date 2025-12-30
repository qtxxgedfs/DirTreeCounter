# DirTreeCounter
A Python script that generates a visual directory tree and counts files/folders in a specified directory.


## Features

- Recursively traverses all subdirectories
- Generates a visual tree structure with icons
- Counts total number of folders and files
- Outputs results to both console and a text file
- Skips hidden files/folders (starting with .)
- Handles permission errors gracefully

## Requirements

- Python 3.6+

## Usage

### Basic Usage

1. Clone this repository
2. Modify the target directory path in the script:
   ```python
   args.path = r"Your\target\directory\path"


### Example
```python
📂 Directory structure: C:\example
============================================================
├── 📁 docs
│   ├── ├── 📄 README.md
│   └── └── 📄 INSTALL.md
├── 📁 src
│   ├── ├── 📁 modules
│   │   └── └── 📄 utils.py
│   └── └── 📄 main.py
└── 📄 .gitignore
============================================================
📊 Statistics:
Total folders: 3
Total files: 4
Total items: 7

✅ Results saved to: C:\scripts\tree-count-directory-stats.txt

