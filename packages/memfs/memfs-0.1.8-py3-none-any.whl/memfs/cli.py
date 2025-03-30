#!/usr/bin/env python
"""
Command-line interface for the memfs virtual filesystem with state persistence.
"""

import argparse
import sys
import json
import os
from memfs import create_fs, __version__
from memfs.memfs import _FS_DATA  # Importujemy bezpośrednio strukturę danych

# Ścieżka do pliku stanu
STATE_FILE = os.path.expanduser("~/.memfs_state.json")


def save_state():
    """Zapisz stan systemu plików do pliku."""
    state = {
        'files': {},
        'dirs': list(_FS_DATA['dirs'])
    }

    # Konwertuj zawartość plików na format, który można zapisać jako JSON
    for path, content in _FS_DATA['files'].items():
        if isinstance(content, bytes):
            # Dla plików binarnych używamy base64
            import base64
            state['files'][path] = {
                'type': 'binary',
                'content': base64.b64encode(content).decode('ascii')
            }
        else:
            state['files'][path] = {
                'type': 'text',
                'content': content
            }

    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)


def load_state():
    """Załaduj stan systemu plików z pliku."""
    if not os.path.exists(STATE_FILE):
        return False

    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)

        # Wyczyść obecny stan
        _FS_DATA['files'].clear()
        _FS_DATA['dirs'] = {'/'}

        # Załaduj katalogi
        for dir_path in state['dirs']:
            _FS_DATA['dirs'].add(dir_path)

        # Załaduj pliki
        for path, file_info in state['files'].items():
            if file_info['type'] == 'binary':
                import base64
                _FS_DATA['files'][path] = base64.b64decode(file_info['content'])
            else:
                _FS_DATA['files'][path] = file_info['content']

        return True
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error loading state: {e}", file=sys.stderr)
        return False


def print_tree(fs, path, indent=""):
    """Print a directory tree."""
    print(f"{indent}{os.path.basename(path) or path}")
    indent += "    "

    # Get directory contents
    try:
        contents = fs.listdir(path)
    except Exception as e:
        print(f"{indent}Error: {e}")
        return

    # First list directories
    for item in sorted(contents):
        item_path = fs.path.join(path, item)
        if fs.isdir(item_path):
            print_tree(fs, item_path, indent)

    # Then list files
    for item in sorted(contents):
        item_path = fs.path.join(path, item)
        if fs.isfile(item_path):
            print(f"{indent}{item}")


def dump_fs(fs, path):
    """Dump the filesystem to a JSON structure."""
    result = {}

    # Add files first
    for root, dirs, files in fs.walk(path):
        for file in files:
            file_path = fs.path.join(root, file)
            try:
                content = fs.readfile(file_path)
                if isinstance(content, bytes):
                    content = content.decode('utf-8', errors='replace')
                result[file_path] = content
            except Exception as e:
                result[file_path] = f"Error: {e}"

    return result


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="memfs - Virtual Filesystem in Memory")
    parser.add_argument('--version', action='version', version=f'memfs {__version__}')

    subparsers = parser.add_subparsers(dest='command', help='Command')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new filesystem')

    # Tree command
    tree_parser = subparsers.add_parser('tree', help='Display filesystem as a tree')
    tree_parser.add_argument('path', nargs='?', default='/', help='Path to display')

    # Touch command
    touch_parser = subparsers.add_parser('touch', help='Create an empty file')
    touch_parser.add_argument('path', help='Path to file')

    # Mkdir command
    mkdir_parser = subparsers.add_parser('mkdir', help='Create a directory')
    mkdir_parser.add_argument('path', help='Path to directory')
    mkdir_parser.add_argument('-p', '--parents', action='store_true', help='Create parent directories as needed')

    # Write command
    write_parser = subparsers.add_parser('write', help='Write content to a file')
    write_parser.add_argument('path', help='Path to file')
    write_parser.add_argument('content', help='Content to write')

    # Read command
    read_parser = subparsers.add_parser('read', help='Read content from a file')
    read_parser.add_argument('path', help='Path to file')

    # Dump command
    dump_parser = subparsers.add_parser('dump', help='Dump filesystem to JSON')
    dump_parser.add_argument('path', nargs='?', default='/', help='Root path to dump')

    args = parser.parse_args()

    # Handle init command specially
    if args.command == 'init':
        # Create a new filesystem
        os.remove(STATE_FILE) if os.path.exists(STATE_FILE) else None
        fs = create_fs()
        save_state()
        print("Initialized new filesystem")
        return 0

    # Load existing state if available
    state_loaded = load_state()

    # Create filesystem instance
    fs = create_fs()

    try:
        if args.command == 'tree':
            print_tree(fs, args.path)

        elif args.command == 'touch':
            with fs.open(args.path, 'w') as f:
                pass
            print(f"Created file: {args.path}")

        elif args.command == 'mkdir':
            if args.parents:
                fs.makedirs(args.path, exist_ok=True)
            else:
                fs.mkdir(args.path)
            print(f"Created directory: {args.path}")

        elif args.command == 'write':
            with fs.open(args.path, 'w') as f:
                f.write(args.content)
            print(f"Wrote to: {args.path}")

        elif args.command == 'read':
            with fs.open(args.path, 'r') as f:
                content = f.read()
            print(content)

        elif args.command == 'dump':
            data = dump_fs(fs, args.path)
            print(json.dumps(data, indent=2))

        else:
            parser.print_help()
            return 1

        # Save state after successful command
        save_state()
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())