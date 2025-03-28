import argparse
import pathspec
import zipfile
from pathlib import Path


def load_gitignore_patterns(zipignore_path: Path) -> pathspec.PathSpec | None:
    """Loads and parses .zipignore patterns"""
    if zipignore_path.exists():
        with open(zipignore_path, "r") as f:
            return pathspec.PathSpec.from_lines("gitwildmatch", f)
    return None


def zip_with_ignore(
    source_folder: str, output_filename: str, zipignore_file: str, prefix: str = ""
) -> None:
    """Creates a zip archive, excluding files matching .zipignore patterns, and adds a prefix inside the archive"""

    source_path = Path(source_folder)
    ignore_spec = load_gitignore_patterns(source_path / zipignore_file)

    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in source_path.rglob("*"):  # Recursively list all files
            if file.is_dir():
                continue  # Skip directories, only add files

            rel_path = file.relative_to(source_path)
            if ignore_spec and ignore_spec.match_file(str(rel_path)):
                continue  # Skip ignored files

            zip_path = Path(prefix) / rel_path if prefix else rel_path  # Apply prefix
            zipf.write(file, zip_path.as_posix())  # Ensure correct path format


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a zip archive with .zipignore support and optional prefix"
    )

    parser.add_argument("source_folder", type=str, help="Folder to zip")
    parser.add_argument(
        "-o",
        "--output_zip",
        type=str,
        default="archive.zip",
        help="Output zip file name (default: archive.zip)",
    )
    parser.add_argument(
        "--ignore-file",
        type=str,
        default=".zipignore",
        help="Ignore file (default: .zipignore)",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default="",
        help="Prefix inside the zip (e.g., 'myproject/')",
    )

    args = parser.parse_args()

    zip_with_ignore(args.source_folder, args.output_zip, args.ignore_file, args.prefix)


if __name__ == "__main__":
    main()
