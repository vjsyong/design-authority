#!/usr/bin/env python3
"""Stdio launcher for the Design Authority MCP server.

Run with the project venv: .venv/bin/python tools/da-mcp.py
Env: DA_PACK (pack dir, default packs/triage), DA_WORKSPACE (gap/proposal +
decision-log location, default cwd).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "kernel"))

from design_authority.mcp_server import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
