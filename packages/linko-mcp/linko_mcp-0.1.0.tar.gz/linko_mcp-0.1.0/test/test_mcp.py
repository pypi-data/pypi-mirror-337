import asyncio
import subprocess
import json
import time

async def test_mcp_tools():
    # Start MCP server
    process = subprocess.Popen(
        ["linko-mcp", "--verbose"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(2)
    
    # Simulate tool call (adjust port if needed)
    tool_call = {
        "name": "get_notes",
        "parameters": {"limit": 2}
    }
    
    # Use httpx or requests to call the local MCP server
    # This is a simplified example
    
    # Close server when done
    process.terminate()
    process.wait()

asyncio.run(test_mcp_tools())