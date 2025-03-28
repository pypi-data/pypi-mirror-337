# Zip Creator with Ignore Support

This Python script creates a zip archive of a folder while respecting an ignore
file (similar to `.gitignore`). It also supports adding a prefix to all files
inside the archive, similar to `git archive --prefix`.

## Features

- Exclude files and folders using a `.zipignore` file (or a custom ignore file)
- Add an optional prefix inside the zip
- Command-line interface for easy use

## Installation

Ensure you have Python >= 3.10 installed and install it with `pipx`:

```bash
pipx install zipcreater-sebastian-stigler
```

## Usage

```bash
zipcreator [-h] [-o OUTPUT_ZIP] [--ignore-file IGNORE_FILE] [--prefix PREFIX] source_folder


positional arguments:
  source_folder         Folder to zip

options:
  -h, --help            show this help message and exit
  -o OUTPUT_ZIP, --output_zip OUTPUT_ZIP
                        Output zip file name (default: archive.zip)
  --ignore-file IGNORE_FILE
                        Ignore file (default: .zipignore)
  --prefix PREFIX       Prefix inside the zip (e.g., 'myproject/')
```

### Examples

#### 1. Basic Usage

```bash
zipcreator my_folder -o output.zip
```

This zips `my_folder` into `output.zip`, using `.zipignore` within `my_folder` to exclude files.

#### 2. Add a Prefix

```bash
zipcreator my_folder -o output.zip --prefix myproject/
```

This adds `myproject/` as a prefix inside the zip.

#### 3. Use a Custom Ignore File

```bash
zipcreator my_folder -o output.zip --ignore-file custom.ignore
```

This uses `custom.ignore` instead of `.zipignore`. (The file has to be stored in `my_folder`.)

## Example `.zipignore` File

```text
# Ignore log files
*.log

# Ignore temporary files
*.tmp
*.bak

# Ignore folders
node_modules/
venv/

# Ignore specific files
secrets.env
debug-output.txt

# Ignore system files
.DS_Store
Thumbs.db

# Ignore __pycache__ directories
__pycache__/

# Ignore build outputs
build/
dist/

# Allow a specific file inside an ignored folder
!dist/readme.txt
```

## Example Output with `--prefix myproject/`

If your original `my_folder` structure is:

```console
my_folder/
│── file1.txt
│── file2.log
│── subdir/
│   └── nested.txt
```

And `.zipignore` contains:

```text
*.log
```

Then `output.zip` will contain:

```console
myproject/file1.txt
myproject/subdir/nested.txt
```

(`file2.log` is ignored due to `.zipignore`)

## Licence

MIT Licence

## Credit

Created with ChatGPT.
