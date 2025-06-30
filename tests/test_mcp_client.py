import os
import pytest
import asyncio
from fastmcp.client import Client
from mcp.shared.exceptions import McpError
from src.main import mcp as server_mcp_instance

PDF_DIR = "/workspaces/mcp_client/pdfs"

@pytest.fixture(scope="module")
def mcp_server_fixture():
    """Provides the configured MCP server instance for testing."""
    os.environ["PDF_DIR"] = PDF_DIR
    # The server instance is already configured upon import
    yield server_mcp_instance

@pytest.mark.asyncio
async def test_server_exposes_pdf_resources(mcp_server_fixture):
    """Tests that the server correctly exposes PDF resources."""
    client = Client(transport=mcp_server_fixture)
    async with client:
        # Test root document
        contents_1 = await client.read_resource("pdf://test_document.pdf")
        assert contents_1 and "This is a test PDF document." in contents_1[0].text

        # Test another root document
        contents_2 = await client.read_resource("pdf://another_document.pdf")
        assert contents_2 and "This is another test file." in contents_2[0].text

        # Test subdirectory document
        contents_3 = await client.read_resource("pdf://subdir/sub_document.pdf")
        assert contents_3 and "This is a document in a subdirectory." in contents_3[0].text

@pytest.mark.asyncio
async def test_server_handles_non_existent_resource(mcp_server_fixture):
    """Tests that the server correctly handles requests for non-existent resources."""
    client = Client(transport=mcp_server_fixture)
    async with client:
        with pytest.raises(McpError, match="Unknown resource"):
            await client.read_resource("pdf://non_existent.pdf")