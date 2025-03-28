import pytest
import asyncio
from mcp_guardian import MCPGuardian

@pytest.mark.asyncio
async def test_valid_token_not_rate_limited():
    guardian = MCPGuardian(valid_tokens={"123"}, max_requests_per_token=5)

    # Mock original_invoke_tool to just return "OK"
    async def mock_invoke_tool(tool_name, *args, **kwargs):
        return "OK"

    guardian.original_invoke_tool = mock_invoke_tool

    response = await guardian.guarded_invoke_tool("some_tool", token="123", param="test")
    assert response == "OK"

@pytest.mark.asyncio
async def test_invalid_token():
    guardian = MCPGuardian(valid_tokens={"123"}, max_requests_per_token=5)

    async def mock_invoke_tool(tool_name, *args, **kwargs):
        return "SHOULD NOT RUN"

    guardian.original_invoke_tool = mock_invoke_tool

    response = await guardian.guarded_invoke_tool("some_tool", token="bad_token")
    assert "Unauthorized" in response
