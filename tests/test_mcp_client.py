import sys
import os
import subprocess
import time
import pytest
import asyncio
from fastmcp.client import Client
from fastmcp.client.transports import PythonStdioTransport

# テスト用のPDFディレクトリ
PDF_DIR = "/workspaces/mcp_client/pdfs"

@pytest.fixture(scope="module")
def mcp_server():
    # サーバープロセスを起動
    env = os.environ.copy()
    env["PDF_DIR"] = PDF_DIR
    env["PYTHONPATH"] = os.pathsep.join([os.getcwd(), env.get("PYTHONPATH", "")])
    process = subprocess.Popen([sys.executable, "run_server.py"], env=env, cwd=os.getcwd())
    time.sleep(25)  # サーバーが起動するまで待機
    yield process
    # テスト終了後にサーバープロセスを終了
    process.terminate()
    process.wait()

@pytest.mark.asyncio
async def test_server_exposes_pdf_resources(mcp_server):
    """サーバーがPDFリソースを正しく公開していることをテストします。"""
    client = Client(transport=PythonStdioTransport(script_path="run_server.py"))
    
    await asyncio.sleep(1) # 非同期sleep

    async with client:
        # test_document.pdf の内容を取得
        resource_id_1 = "pdf://test_document.pdf"
        contents_1 = await client.read_resource(resource_id_1) # read_resource を使用
        assert contents_1 is not None
        assert len(contents_1) > 0
        assert "This is a test PDF document." in contents_1[0].text

        # another_document.pdf の内容を取得
        resource_id_2 = "pdf://another_document.pdf"
        contents_2 = await client.read_resource(resource_id_2) # read_resource を使用
        assert contents_2 is not None
        assert len(contents_2) > 0
        assert "This is another test file." in contents_2[0].text

@pytest.mark.asyncio
async def test_server_handles_non_existent_resource(mcp_server):
    """存在しないリソースのリクエストをサーバーが処理できることをテストします。"""
    client = Client(transport=PythonStdioTransport(script_path="run_server.py"))
    await asyncio.sleep(1)
    async with client:
        resource_id = "pdf://non_existent.pdf"
        contents = await client.read_resource(resource_id) # read_resource を使用
        # 存在しないリソースの場合、空のリストが返されるか、text='null' のオブジェクトが返される
        assert contents is not None
        assert len(contents) == 0 or (len(contents) == 1 and contents[0].text == 'null')