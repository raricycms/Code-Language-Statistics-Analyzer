#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from collections import defaultdict
import sys

# This script requires:
# - 'pathspec' for .gitignore support (optional): pip install pathspec
# - 'rich' for beautiful table output (optional): pip install rich
try:
    import pathspec
except ImportError:
    pathspec = None

try:
    from rich.console import Console
    from rich.table import Table
except ImportError:
    Console = None
    Table = None

# A mapping of file extensions to programming languages.
# Feel free to extend this list for your project's needs.
LANGUAGE_MAP = {
    # Web Front-end
    '.html': 'HTML',
    '.htm': 'HTML',
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.sass': 'Sass',
    '.js': 'JavaScript',
    '.jsx': 'JavaScript (JSX)',
    '.ts': 'TypeScript',
    '.tsx': 'TypeScript (TSX)',
    '.vue': 'Vue',

    # Python
    '.py': 'Python',
    '.pyw': 'Python',
    '.pyi': 'Python',
    '.mako': 'Mako',

    # C Family
    '.c': 'C',
    '.h': 'C',
    '.cpp': 'C++',
    '.hpp': 'C++',
    '.cxx': 'C++',
    '.hxx': 'C++',
    '.cs': 'C#',

    # Java & JVM
    '.java': 'Java',
    '.kt': 'Kotlin',
    '.kts': 'Kotlin Script',
    '.scala': 'Scala',
    '.groovy': 'Groovy',

    # Other Languages
    '.go': 'Go',
    '.rs': 'Rust',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.swift': 'Swift',
    '.pl': 'Perl',
    '.sh': 'Shell',
    '.bat': 'Batch',
    '.ps1': 'PowerShell',
    '.sql': 'SQL',

    # Config & Data
    '.json': 'JSON',
    '.xml': 'XML',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.ini': 'INI',
    '.toml': 'TOML',
    '.md': 'Markdown',
    '.rst': 'reStructuredText',
    
    # Docker
    'Dockerfile': 'Docker',
}

def get_language(file_path):
    """Detects the language of a file based on its extension or name."""
    file_name = os.path.basename(file_path)
    if file_name in LANGUAGE_MAP:
        return LANGUAGE_MAP[file_name]
    
    _, ext = os.path.splitext(file_name)
    if ext:
        return LANGUAGE_MAP.get(ext.lower())
    return None

def get_gitignore_spec(project_path):
    """Loads and parses the .gitignore file from the project path."""
    gitignore_path = os.path.join(project_path, '.gitignore')
    if pathspec and os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            return pathspec.PathSpec.from_lines('gitwildmatch', f)
    return None

def analyze_project(project_path, use_gitignore):
    """Analyzes the project directory and returns language statistics."""
    stats = defaultdict(lambda: {'lines': 0, 'files': 0})
    
    ignore_spec = None
    if use_gitignore:
        if not pathspec:
            print("Warning: 'pathspec' library not found. --gitignore option is disabled.", file=sys.stderr)
            print("Install it with: pip install pathspec", file=sys.stderr)
        else:
            ignore_spec = get_gitignore_spec(project_path)

    for root, dirs, files in os.walk(project_path, topdown=True):
        if ignore_spec:
            rel_root = os.path.relpath(root, project_path)
            if rel_root == '.':
                rel_root = ''
            original_dirs = dirs[:]
            dirs[:] = [d for d in original_dirs if not ignore_spec.match_file(os.path.join(rel_root, d))]

        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, project_path).replace('\\', '/')
            if ignore_spec and ignore_spec.match_file(relative_path):
                continue
            
            language = get_language(file_path)
            if language:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        line_count = sum(1 for _ in f)
                        stats[language]['lines'] += line_count
                        stats[language]['files'] += 1
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}", file=sys.stderr)
    
    return stats

def print_results_rich(stats, console):
    """Prints the language statistics using a rich Table."""
    sorted_stats = sorted(stats.items(), key=lambda item: item[1]['lines'], reverse=True)
    total_lines = sum(data['lines'] for _, data in sorted_stats)
    total_files = sum(data['files'] for _, data in sorted_stats)

    table = Table(title="Code Language Statistics", show_footer=True, footer_style="bold cyan")
    table.add_column("Language", style="magenta", footer="Total")
    table.add_column("Files", justify="right", style="green", footer=f"{total_files:,}")
    table.add_column("Lines of Code", justify="right", style="cyan", footer=f"{total_lines:,}")
    table.add_column("Percentage", justify="right", style="yellow", footer="100.00%")

    for lang, data in sorted_stats:
        percentage = (data['lines'] / total_lines * 100) if total_lines > 0 else 0
        table.add_row(
            lang,
            f"{data['files']:,}",
            f"{data['lines']:,}",
            f"{percentage:.2f}%"
        )
    console.print(table)

def print_results_plain(stats):
    """Prints the language statistics in a plain text table."""
    sorted_stats = sorted(stats.items(), key=lambda item: item[1]['lines'], reverse=True)
    total_lines = sum(data['lines'] for lang, data in sorted_stats)
    total_files = sum(data['files'] for lang, data in sorted_stats)

    max_lang_len = max(len(lang) for lang, data in sorted_stats) if sorted_stats else 10
    max_lang_len = max(max_lang_len, len("Language"))

    print(f"\n{'Language':<{max_lang_len}} | {'Files':>8} | {'Lines':>12} | {'Percentage':>12}")
    print(f"{'-' * max_lang_len}-|----------|--------------|-------------")

    for lang, data in sorted_stats:
        percentage = (data['lines'] / total_lines * 100) if total_lines > 0 else 0
        print(f"{lang:<{max_lang_len}} | {data['files']:>8} | {data['lines']:>12} | {percentage:11.2f}%")

    print(f"{'-' * max_lang_len}-|----------|--------------|-------------")
    print(f"{'Total':<{max_lang_len}} | {total_files:>8} | {total_lines:>12} | {'100.00%':>11}")

def print_results(stats):
    """Prints results, choosing rich or plain output based on availability."""
    if not stats:
        if Console:
            Console().print("[yellow]No code files were found or analyzed.[/yellow]")
        else:
            print("No code files were found or analyzed.")
        return

    if Console and Table:
        print_results_rich(stats, Console())
    else:
        print_results_plain(stats)

def main():
    """Main function to parse arguments and run the analysis."""
    parser = argparse.ArgumentParser(
        description="Analyzes a project's source code and reports language statistics.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'path', nargs='?', default='.',
        help='The path to the project directory to analyze (default: current directory).'
    )
    parser.add_argument(
        '--gitignore', action='store_true',
        help='If set, respects the .gitignore file in the project directory.'
    )
    args = parser.parse_args()

    project_path = os.path.abspath(args.path)

    if not os.path.isdir(project_path):
        print(f"Error: Path '{project_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    if Console:
        console = Console()
        console.print(f"Analyzing project at: [bold cyan]{project_path}[/bold cyan]")
        if args.gitignore:
            console.print("Ignoring files specified in .gitignore.", style="italic yellow")
        console.rule()
    else:
        print(f"Analyzing project at: {project_path}")
        if args.gitignore:
            print("Ignoring files specified in .gitignore.")
        print("-" * 40)
        print("Hint: For a more beautiful output, install the 'rich' library: pip install rich", file=sys.stderr)

    stats = analyze_project(project_path, args.gitignore)
    print_results(stats)

if __name__ == '__main__':
    main()