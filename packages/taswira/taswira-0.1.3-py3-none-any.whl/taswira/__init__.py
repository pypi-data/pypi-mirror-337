"""A command-line tool for visualizing GCBM output."""
from .scripts.console import console

__version__ = "0.1.3"


def main():
    """Entry point for the CLI"""
    console()
