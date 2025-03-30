#!/usr/bin/env python3
"""
test_main.py

Example script to:
1) Load MCP server configuration
2) Connect over stdio_client
3) Initialize and ping the server
4) List available tools
"""

import logging
import sys
import anyio

# mcp imports (adjust if you renamed or reorganized):
from mcp_client.messages.initialize.send_messages import send_initialize
from mcp_client.messages.ping.send_messages import send_ping
from mcp_client.messages.tools.send_messages import send_tools_list
from mcp_client.transport.stdio.stdio_client import stdio_client

# If 'mcp_cli.config' is in your codebase (from the snippet),
# adjust import path as needed:
try:
    from mcp_cli.config import load_config
except ImportError:
    print("Warning: Could not import 'mcp_cli.config'. Check your paths or comment out load_config if not needed.")
    load_config = None

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

async def main():
    """
    Minimal demonstration of connecting to an MCP server via stdio,
    initializing, and sending a ping + listing tools.
    """
    # Example configuration parameters
    config_path = "server_config.json"
    server_name = "sqlite"

    # If you have a real config loader, use it:
    if load_config:
        server_params = await load_config(config_path, server_name)
    else:
        # Fallback if mcp_cli.config isn't available:
        server_params = {
            "config_path": config_path,
            "server_name": server_name
            # add any other parameters your stdio_client expects
        }
    
    async with stdio_client(server_params) as (read_stream, write_stream):
        # 1) Initialize the server
        init_result = await send_initialize(read_stream, write_stream)
        if not init_result:
            print("Server initialization failed.")
            return
        
        print("Initialization successful!")

        # 2) Send a ping
        ping_result = await send_ping(read_stream, write_stream)
        if ping_result:
            print("Ping successful!")
        else:
            print("Ping failed.")

        # 3) Retrieve the tools list
        tools_result = await send_tools_list(read_stream, write_stream)
        print(f"Tools result: {tools_result}")

if __name__ == "__main__":
    anyio.run(main)
