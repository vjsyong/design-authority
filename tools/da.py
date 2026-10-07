#!/usr/bin/env python3
"""Thin launcher: python3 tools/da.py <cmd>  (adds kernel/ to sys.path)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "kernel"))

from design_authority.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
