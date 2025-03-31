#!/usr/bin/env python3
"""
Entry point script for kb-build command.
"""

import sys

from kb_builder.cli import main as cli_main

def main():
    """
    Main entry point for kb-build command.
    
    This function modifies sys.argv to include the "build" command
    and then calls the main function from cli.py, ensuring it uses
    the same execution path as `python -m kb_builder build`.
    """
    # Save the original program name
    prog_name = sys.argv[0]
    
    # Modify sys.argv to include the "build" command as the first argument
    # This makes it behave as if it was called as `python -m kb_builder build [args]`
    sys.argv = [prog_name, "build"] + sys.argv[1:]
    
    # Call the main function from cli.py
    # This will parse the arguments and call the appropriate function (build_command)
    cli_main()

if __name__ == "__main__":
    main()
