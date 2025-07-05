"""
Pipetrace - A lightweight Python tool for tracing program control flow using named pipes (FIFOs).
"""

__version__ = "0.1.0"

from .pipetrace import trace, logger

__all__ = ["trace", "logger"]