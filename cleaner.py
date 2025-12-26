import argparse
import shutil
import os
from pathlib import Path


# Common folders that usually can be safely removed
JUNK_FOLDERS = {
    "node_modules",
    "__pycache__",
    "dist",
    "build",
    ".gradle",
    ".idea",
    ".vscode"
}


def get_folder_size(path: Path) -> int:
    total_size = 0
    for root, _, files in os.walk(path):
        for file in files:
            try:
                file_path = Path(root) / file
                total_size += file_path.stat().st_size
            except (OSError, PermissionError):
                pass
    return total_size


def analyze_project(project_path: Path):
    found_folders = []

    for item in project_path.rglob("*"):
        if not item.is_dir():
            continue

        if item.name not in JUNK_FOLDERS:
            continue

        if any(parent in item.parents for parent, _ in found_folders):
            continue

        size = get_folder_size(item)
        found_folders.append((item, size))

    return found_folders


def format_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


def confirm_deletion():
    answer = input(
        "\n⚠️ This will permanently delete the listed folders. Continue? (y/N): "
    ).strip().lower()
    return answer == "y"


def delete_folders(folders, dry_run=False):
    for folder, _ in folders:
        if dry_run:
            print(f"[DRY-RUN] Would delete: {folder}")
        else:
            try:
                shutil.rmtree(folder)
                print(f"🗑️ Deleted: {folder}")
            except (OSError, PermissionError) as e:
                print(f"❌ Failed to delete {folder}: {e}")


def show_menu():
    print("\nWhat do you want to do?")
    print("1) Delete junk folders")
    print("2) Dry-run (simulate deletion)")
    print("0) Exit")

    return input("\nSelect an option: ").strip()


def get_project_path_from_user():
    print("📂 Drag and drop a project folder here and press Enter")
    print("   (or paste the path manually)\n")
    path = input("> ").strip('"').strip()
    return Path(path)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze a project directory and detect unnecessary folders."
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Path to the project directory"
    )

    args = parser.parse_args()

    if args.path:
        project_path = Path(args.path)
    else:
        project_path = get_project_path_from_user()

    if not project_path.exists():
        print("❌ The provided path does not exist.")
        return

    if not project_path.is_dir():
        print("❌ The provided path is not a directory.")
        return

    print(f"\n🔍 Analyzing project: {project_path}\n")

    junk_folders = analyze_project(project_path)

    if not junk_folders:
        print("✅ No junk folders found.")
        return

    junk_folders.sort(key=lambda item: item[1], reverse=True)

    total_size = 0
    print("Found junk folders:\n")

    for folder, size in junk_folders:
        relative_path = folder.relative_to(project_path)
        print(f"{str(relative_path):<40} → {format_size(size)}")
        total_size += size

    print("-" * 60)
    print(f"Total space used: {format_size(total_size)}")

    # Menu loop (only exits with option 0)
    while True:
        choice = show_menu()

        if choice == "1":
            if confirm_deletion():
                delete_folders(junk_folders)

        elif choice == "2":
            delete_folders(junk_folders, dry_run=True)

        elif choice == "0":
            print("👋 Exiting.")
            break

        else:
            print("❌ Invalid option.")


if __name__ == "__main__":
    main()
