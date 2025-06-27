#!/usr/bin/env python3
"""
Entry point for running the LetsCloud MCP Server as a module.

Usage:
    python -m src.letscloud_mcp_server
"""

import asyncio
from .server import main

if __name__ == "__main__":
    asyncio.run(main()) 