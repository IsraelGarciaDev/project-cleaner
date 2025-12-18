# Project Cleaner & Analyzer

A lightweight Python tool to analyze project folders and detect unnecessary files and directories that usually take up a lot of disk space (builds, cache, dependencies).

## Motivation

In many projects, folders like `node_modules`, `__pycache__`, `dist` or `build` tend to accumulate over time.  
They are not required for day-to-day development, but they can take up a noticeable amount of disk space.

This script was created as a simple way to:
- Analyze a project directory
- Understand how much disk space it actually uses
- Decide what can be safely removed

## What does it do at the moment?

- Analyzes a user-defined path
- Detects common folders considered junk
- Calculates the size of each one
- Shows a clear summary in the console

> ⚠️ At the moment, it does not delete anything — it only analyzes and displays information.

## Technologies used

- Python 3
- Standard libraries (`os`, `pathlib`, `shutil`, `argparse`)

No external dependencies are required.

## Usage

```bash
python cleaner.py C:\path\to\your\project
```

## Possible Future Improvements

- Add command-line flags (`--dry-run`, `--delete`, `--verbose`)
- Interactive confirmation before deleting files
- Configuration via JSON file
- Execution logs
- Basic unit tests
- Optional conversion to a standalone executable
