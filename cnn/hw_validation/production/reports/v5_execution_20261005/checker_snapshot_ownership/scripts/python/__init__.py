"""Extend the original runtime without modifying the installed package."""
from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
