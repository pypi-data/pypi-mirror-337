#!/usr/bin/env python3
import sys
import os

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False

def main():
    """
    Usage:
      vibez [-s "Your summary"] [-o <output.md>] [-r] [-i "item1,item2,..."] <file|file:range|directory> [<file|file:range|directory> ...]
    """

    if len(sys.argv) < 2:
        print("Usage: vibez [-s \"Your summary\"] [-o <output.md>] [-r] [-i \"item1,item2,...\"] <file|file:range|directory> [<file|file:range|directory> ...]")
        sys.exit(1)

    args = sys.argv[1:]
    output_file = None
    recursive = False
    summary = None
    ignore_list = set()
    file_specs = []

    flag_aliases = {
        '-r': '--recursive',
        '-i': '--ignore',
        '-o': '--output',
        '-s': '--summary'
    }
    args = [flag_aliases.get(arg, arg) for arg in args]

    # Recursive flag
    if '--recursive' in args:
        recursive = True
        args.remove('--recursive')

    # Ignore flag
    if '--ignore' in args:
        ignore_index = args.index('--ignore')
        if ignore_index + 1 >= len(args):
            print("Error: You used '--ignore' but did not specify any files or directories.")
            sys.exit(1)
        ignore_list.update(args[ignore_index + 1].split(','))
        del args[ignore_index:ignore_index + 2]

    # Output file flag
    if '--output' in args:
        output_index = args.index('--output')
        if output_index + 1 >= len(args):
            print("Error: You used '--output' but did not specify an output file.")
            sys.exit(1)
        output_file = args[output_index + 1]
        del args[output_index:output_index + 2]

    # Summary flag
    if '--summary' in args:
        summary_index = args.index('--summary')
        if summary_index + 1 >= len(args):
            print("Error: You used '--summary' but did not provide a summary.")
            sys.exit(1)
        summary = args[summary_index + 1]
        del args[summary_index:summary_index + 2]

    # File specs
    file_specs = args

    if not file_specs:
        print("Error: No files or directories specified.")
        sys.exit(1)

    if output_file is None and not PYPERCLIP_AVAILABLE:
        print("Error: pyperclip is not installed for clipboard copying. Install via 'pip install pyperclip',")
        print("or use the '-o <OUTPUT.md>' option to write to a file instead.")
        sys.exit(1)

    content = []

    def add_snippet_block(header, snippet):
        if snippet.strip():
            content.append(f"{header}:\n```\n{snippet}\n```\n")

    def process_file(filepath, line_range=None):
        if filepath in ignore_list:
            print(f"Ignoring: {filepath}")
            return

        if not os.path.isfile(filepath):
            print(f"Skipping: file '{filepath}' not found.")
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f_in:
                content_lines = f_in.readlines()
        except UnicodeDecodeError:
            print(f"Skipping non-UTF-8 file: {filepath}")
            return

        if line_range:
            start_line, end_line = line_range
            file_length = len(content_lines)
            start_line = max(1, start_line)
            end_line = min(file_length, end_line)
            excerpt = content_lines[start_line - 1:end_line]
            excerpt_str = "".join(excerpt)
            add_snippet_block(f"{filepath} (lines {start_line}-{end_line})", excerpt_str)
        else:
            file_content = "".join(content_lines)
            add_snippet_block(filepath, file_content)

    def process_directory(directory):
        for root, _, files in os.walk(directory):
            if root in ignore_list:
                print(f"Ignoring directory: {root}")
                continue

            for file in files:
                filepath = os.path.join(root, file)
                if filepath in ignore_list:
                    print(f"Ignoring file: {filepath}")
                    continue
                process_file(filepath)

            if not recursive:
                break

    for spec in file_specs:
        if ':' in spec:
            parts = spec.split(':', 1)
            filename = parts[0]
            line_range = parts[1]

            if '-' not in line_range:
                print(f"Skipping invalid line range format: {line_range}")
                continue

            try:
                start_line, end_line = map(int, line_range.split('-'))
            except ValueError:
                print(f"Skipping invalid numeric range: {line_range}")
                continue

            process_file(filename, (start_line, end_line))
        elif os.path.isdir(spec):
            process_directory(spec)
        else:
            process_file(spec)

    concatenated_content = "".join(content)

    if summary:
        concatenated_content = f"{summary}\n\n{concatenated_content}"

    if output_file is None:
        pyperclip.copy(concatenated_content)
        print("Contents copied to clipboard.")
    else:
        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.write(concatenated_content)
            print(f"Created {output_file}.")

if __name__ == '__main__':
    main()
