#!/usr/bin/env python3
"""
Entry point for running the LetsCloud MCP Server as a module.

Usage:
    python -m letscloud_mcp_server [--version] [--help]
"""

import argparse
import asyncio
import sys
from .server import main

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="LetsCloud MCP Server - Manage LetsCloud infrastructure via MCP",
        prog="letscloud-mcp-server"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="letscloud-mcp-server 1.0.0"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    if args.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    asyncio.run(main()) 