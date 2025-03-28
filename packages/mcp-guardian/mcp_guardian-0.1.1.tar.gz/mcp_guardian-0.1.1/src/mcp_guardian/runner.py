import sys
import json
import asyncio
from typing import Any

from mcp.server.fastmcp import FastMCP
from .guardian import MCPGuardian

class StdioGuardedRunner:
    """
    A custom runner that:
      1) Reads JSON requests from stdin.
      2) Calls MCPGuardian for security checks + logging.
      3) Invokes the corresponding tool in a FastMCP instance if allowed.
      4) Returns a JSON response to stdout.
    """

    def __init__(self, mcp: FastMCP, guardian: MCPGuardian):
        """
        Args:
            mcp: A FastMCP instance with tools registered via @mcp.tool().
            guardian: An MCPGuardian instance for security + logging.
        """
        self.mcp = mcp
        self.guardian = guardian

    async def handle_request(self, request: dict) -> dict:
        """
        Processes a single request from the client.
        Returns a dict that can be JSON-serialized (the response).
        """
        tool_name = request.get("tool")
        args = request.get("args", {})

        # 1) Find the tool
        tool_meta = self.mcp._tools.get(tool_name)
        if not tool_meta:
            return {"error": f"Tool '{tool_name}' not found."}

        # 2) Guardian checks
        error_msg = self.guardian.check_and_log(tool_name, args)
        if error_msg:
            # Return an error response
            return {"error": error_msg}

        # 3) Actually call the tool function
        tool_func = tool_meta.func
        try:
            # tool_func is async, so we await it
            result = await tool_func(**args)
        except Exception as e:
            return {"error": str(e)}

        # 4) Log the response
        token = args.get("token", "N/A")
        self.guardian.log_response(tool_name, token, result)

        # 5) Return success
        return {"result": result}

    async def run_stdio(self):
        """
        Main loop: read lines from stdin, handle each request, print JSON output.
        """
        while True:
            line = sys.stdin.readline()
            if not line:
                break  # EOF or stream closed

            line = line.strip()
            if not line:
                continue  # skip empty lines

            try:
                request = json.loads(line)
            except json.JSONDecodeError:
                response = {"error": "Invalid JSON request."}
                print(json.dumps(response), flush=True)
                continue

            # Handle request
            response_data = await self.handle_request(request)
            print(json.dumps(response_data), flush=True)

    def run(self):
        """Convenience method to run the stdio loop in an asyncio event loop."""
        asyncio.run(self.run_stdio())
