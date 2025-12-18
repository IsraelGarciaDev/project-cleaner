import argparse
import os
from pathlib import Path

#Common folders that usually can be safely removed
JUNK_FOLDERS = {
    "node_modules",
    "__pycache__",
    "dist",
    "build",
    ".gardle",
    ".idea",
    ".vscode"
}

def get_folder_size(path: Path) -> int:
    #Calculates the total size of a folder recursively and returns size in bytes
    total_size = 0

    for root, _, files in os.walk(path):
        for file in files:
            try:
                file_path = Path(root)/file
                total_size += file_path.stat().st_size
            except (OSError, PermissionError):
                #Skip files we cant access
                pass

    return total_size

def analyze_project(project_path: Path):
    found_folders =[]

    for item in project_path.rglob("*"):
        if item.is_dir() and item.name in JUNK_FOLDERS:
            size = get_folder_size(item)
            found_folders.append((item,size))

    return found_folders

def format_size(size_bytes: int ) -> str:

    #Converts bytes to a readable format
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

def main():
    parser = argparse.ArgumentParser(
        description = "Analyze a project directory and detect unnecesary folders:"
    )
    parser.add_argument(
        "path",
        help = "Path to the project directory"
    )

    args = parser.parse_args()
    project_path = Path(args.path)

    if not project_path.exists():
        print("❌ The provided path does not exist.")
        return

    if not project_path.is_dir():
        print("❌ The provided path is not a directory.")
        return

    print(f"🔍 Analyzing project: {project_path}\n")

    junk_folders = analyze_project(project_path)

    if not junk_folders:
        print("✅ No junk folders found.")
        return

    total_size = 0

    for folder, size in junk_folders:
        print(f"{folder.name:<15} -> {format_size(size)}")
        total_size += size

    print("-" * 30)
    print(f"Total space used: {format_size(total_size)}")

if __name__ == "__main__":
    main()