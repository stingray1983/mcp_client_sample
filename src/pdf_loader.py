import os
import pdfplumber
from typing import List

def find_pdfs(directory: str) -> List[str]:
    """指定されたディレクトリ内のすべてのPDFファイルを検索します。"""
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".pdf")]

def extract_text_from_pdf(pdf_path: str) -> str:
    """単一のPDFファイルからテキストコンテンツを抽出します。"""
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
