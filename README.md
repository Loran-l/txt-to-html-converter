Converts txt and .md to plane html static site

## Features

| Command | Description |
| ------- | ----------- |
| `--help`/`-h` | Display the full list of features |
| `--version`/`-v` | Check the tool version |
| `--input`/`-i <INPUT_FILE_OR_FOLDER>` | Specify input file or folder |
| `--output`/`-o <OUTPUT_FOLDER>` | Specify output folder (default is `./dist`) |
| `--lang`/`-l <LANGUAGE_CODE>` | Specify language for output file(s) (default is `en`) |
| `--encoding`/`-e <ENCODING_NAME>` | Specify character encoding (default is `utf-8`) |
| `--config`/`-c <CONFIG_JSON_FILE>` | Load custom configuration from a JSON file |

## Installation

> Make sure you have installed Python version 3.8.5 or above.

## How to use

1. Generate a .html file from a file or folder:

   > ` python txt-to-html.py -i/--input <file name or folder name>`

2. Check the tool's version

   > ` python txt-to-html.py –v/--version`

3. Display how to use the tool
   > ` python txt-to-html.py –h`

## Example

> `python txt-to-html.py -i test2.md

> `python txt-to-html.py -i test.txt

