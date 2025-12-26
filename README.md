# Project Cleaner & Analyzer

A lightweight Python tool to analyze project folders and safely remove common unnecessary directories that tend to take up a lot of disk space (builds, cache, dependencies).

This repository contains a simple, single-file Python script (cleaner.py) that can be used interactively from the console. It is also straightforward to package as a standalone Windows executable (e.g. with PyInstaller).


This README reflects the actual behavior of the included script (the current implementation in cleaner.py). It documents what the script does today, how to use it, and which features are not yet implemented but could be added in the future.

---

## Motivation

In many development projects, folders like `node_modules`, `__pycache__`, `dist` or `build` accumulate over time. They are not required for day-to-day development or for version control, but they can consume a significant amount of disk space.

This tool was created to:
- Analyze a project directory
- Identify common junk folders
- Measure how much disk space they take
- Allow the user to remove them safely via an interactive confirmation

---

## Prerequisites

- Python 3.8 or newer is recommended.
- No extra packages required.

Check your Python version:
```bash
python --version
```

---

## Usage 
Note: If the project folder does not have any supported junk folders, it will automaticly close
### Exe
Run the executable and instructions will be shown on a terminal


### Python script

The script accepts an optional positional path argument. If you omit the path, the script prompts you to paste or drag-and-drop a project folder path into the console.

Windows example:
```bash
python cleaner.py "C:\path\to\your\project"
```

macOS / Linux example:
```bash
python3 cleaner.py "/path/to/your/project"
```
---

## Building a Windows Executable (optional if you modify the code)

You can package the script as a single-file executable using PyInstaller. Example:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build single-file executable:

>In the root folder of the script
```bash
pyinstaller --onefile cleaner.py
```

3. The executable will appear in `dist/cleaner.exe`.

---

## Supported Junk Folders (built-in defaults)

The script currently looks for directories with these names:

- node_modules
- __pycache__
- dist
- build
- .gradle
- .idea
- .vscode

You can extend or change this list by editing the JUNK_FOLDERS set in cleaner.py.

---

## Current Features

- Recursively scans a provided project directory for commonly "junk" folder names.
- Detects folders whose name matches the built-in junk list (see Supported Junk Folders).
- Calculates the disk usage of each detected folder by walking files and summing sizes.
- Shows a sorted summary in the console (largest first).
- Interactive console menu (after scan) with options:
  - Delete junk folders (requires explicit confirmation; deletes permanently using shutil.rmtree)
  - Dry-run (simulate deletion; lists what would be removed without removing anything)
  - Exit
- Attempts to avoid duplicate/deep-nested double-reporting by skipping a folder if a previously recorded folder is an ancestor (best-effort).
- Safe-by-default: nothing is deleted unless the user explicitly confirms via the interactive prompt.

Important limitations in the current script:
- There are no command-line flags other than an optional positional path argument. (No `--dry-run`, `--delete`, `--yes`, `--config`, or `--verbose` flags are implemented at this time.)
- No JSON configuration file support is implemented in the script (the README previously suggested a config option — that is currently not present).
- No exclude-paths or builtin exclusions except the hardcoded junk names.
- Deletion is permanent (uses shutil.rmtree). There is no recycle/trash/recover implementation.

---

## Possible Future Improvements (not implemented in the current script)

- Add command-line flags: `--dry-run`, `--delete`, `--yes`, `--verbose`, `--config`
- Support a JSON config file for junk names and exclude paths
- Add `--exclude-paths` to skip specific directories (venv, .git, etc.)
- Add logging to a file with verbosity levels and rotation
- Unit tests and CI
- Performance improvements (parallel size calculation)
- Optional GUI or cross-platform packaged executables
- Implement safe deletion options (move to recycle bin / create backups)

---
