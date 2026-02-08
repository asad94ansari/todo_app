#!/usr/bin/env python3
"""
Main entry point for the in-memory console todo application.
"""
try:
    from implementation.cli import TodoCLI
except ImportError:
    from cli import TodoCLI


def main():
    """Entry point for the application."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()