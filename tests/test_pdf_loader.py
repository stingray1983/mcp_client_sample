
import os
from src.pdf_loader import find_pdfs, extract_text_from_pdf

TEST_DATA_DIR = "/workspaces/mcp_client/tests/test_data"

def test_find_pdfs():
    """PDFファイルのみが検出されることをテストします。"""
    pdf_files = find_pdfs(TEST_DATA_DIR)
    assert len(pdf_files) == 2
    assert all(f.endswith(".pdf") for f in pdf_files)
    assert os.path.join(TEST_DATA_DIR, "test_document.pdf") in pdf_files
    assert os.path.join(TEST_DATA_DIR, "another_document.pdf") in pdf_files

def test_extract_text_from_pdf():
    """PDFからテキストが正しく抽出されることをテストします。"""
    pdf_path = os.path.join(TEST_DATA_DIR, "test_document.pdf")
    text = extract_text_from_pdf(pdf_path)
    assert "This is a test PDF document." in text
