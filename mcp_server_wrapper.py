#!/usr/bin/env python3
"""
MCP Server Wrapper for Inspector Compatibility
This script handles common MCP inspector arguments and launches the server.
"""

import argparse
import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments, handling common MCP inspector options."""
    parser = argparse.ArgumentParser(description="Fantasy Football MCP Server Wrapper")
    
    # Common MCP inspector arguments
    parser.add_argument("--directory", "-d", type=str, help="Working directory (ignored)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    # Parse known args only, ignore unknown ones
    args, unknown = parser.parse_known_args()
    
    if unknown:
        logger.info(f"Ignoring unknown arguments: {unknown}")
    
    return args

def main():
    """Main entry point for the MCP server wrapper."""
    args = parse_arguments()
    
    # Handle --directory argument (change working directory if needed)
    if args.directory:
        logger.info(f"Ignoring --directory argument: {args.directory}")
        logger.info(f"Current working directory: {os.getcwd()}")
    
    # Set log level
    if args.verbose or args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Verbose logging enabled")
    
    # Import and run the actual MCP server
    try:
        from app.server_with_args import mcp
        logger.info("Starting Fantasy Football MCP Server...")
        logger.info("Available tools: get_nfl_injuries, get_player_ratings, get_player_ratings_by_source, get_player_ratings_by_position, get_player_ratings_by_team")
        mcp.run()
    except ImportError as e:
        logger.error(f"Failed to import MCP server: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
