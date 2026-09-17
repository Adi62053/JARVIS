"""
JARVIS Permanent Launcher

This file always launches the currently active
version-specific JARVIS runtime.

Current active version:
V8

Normal startup command:
    python start_jarvis.py
"""

import sys

from main_v8 import main


if __name__ == "__main__":
    command = " ".join(sys.argv[1:]).strip()
    main(command if command else None)
