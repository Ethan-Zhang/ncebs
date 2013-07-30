import sys


def import_module(import_str):
    """Import a module."""

    __import__(import_str)
    return sys.modules[import_str]

