<p align="center">
  <img src="https://github.com/user-attachments/assets/58a0f433-2271-49c8-ad80-3f56f060fce4" alt="Demo" />
</p>

## Overview

`vibez` is a command-line tool that extracts file contents for use with LLMs.

## Motivation

The developer AI workflow is messy. There are _many_ tools that integrate across the different stages of development and layers of the stack. Some are more powerful, but heavyweight and expensive. For most prompts, you only need a limited amount of [context](https://en.wikipedia.org/wiki/Large_language_model#Prompt_engineering,_attention_mechanism,_and_context_window). `vibez` is a pragmatic solution to this problem. Simply copy the file contents you need and use whatever AI tool you prefer.

## Installation

Install with `pip`:

```sh
pip install vibez
```

Or install from source:

```sh
git clone https://github.com/williamgrosset/vibez.git
cd vibez
pip install .
```

## Usage

```sh
vibez [OPTIONS] <file|file:range|directory> [...]
```

### Options

- `[-r | --recursive]`: Recursively process directories.
- `[-i | --ignore] "item1,item2,..."`: Ignore files or directories.
- `[-o | --output] <output.md>`: Save output to a file.
- `[-s | --summary] "Your summary"`: Add a summary.

### Examples

#### Extract a single file to clipboard

```sh
vibez file.py
```

#### Extract specific lines from a file

```sh
vibez file.py:5-15
```

#### Extract multiple files and directories

```sh
vibez notes.md file.py src/
```

#### Recursively extract from a directory

```sh
vibez -r src/
```

#### Ignore files or directories

```sh
vibez -r dir/ -i "dir/.gitignore,dir/.git"
```

#### Save output to a file

```sh
vibez -o output.md file.py
```

#### Add a summary

```sh
vibez -s "Add login functionality" auth.py
```

### Output Format

````md
<summary>

<file-1> (line range):

```
<content>
```

<file-2> (line range):

```
<content>
```

...

<file-n> (line range):

```
<content>
```
````

## License

MIT
