import os
import pdfplumber
from typing import List

def find_pdfs(directory: str) -> List[str]:
    """指定されたディレクトリとそのサブディレクトリ内のすべてのPDFファイルを再帰的に検索します。"""
    pdf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

def extract_text_from_pdf(pdf_path: str) -> str:
    """単一のPDFファイルからテキストコンテンツを抽出します。"""
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
