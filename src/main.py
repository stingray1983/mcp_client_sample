import os
from fastmcp import FastMCP
from src.pdf_loader import find_pdfs, extract_text_from_pdf

mcp = FastMCP(name="PDFResourceServer")

@mcp.resource("pdf://{filename}")
def get_pdf_resource(filename: str):
    pdf_dir = os.environ.get("PDF_DIR", "./pdfs") # 環境変数からPDFディレクトリを取得、デフォルトは./pdfs
    pdf_path = os.path.join(pdf_dir, filename)

    if not os.path.exists(pdf_path) or not pdf_path.endswith(".pdf"):
        return None # リソースが見つからない場合はNoneを返す

    try:
        content = extract_text_from_pdf(pdf_path)
        return content
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None



if __name__ == "__main__":
    # サーバー起動時にPDFをスキャンし、利用可能なリソースをログに出力
    pdf_dir = os.environ.get("PDF_DIR", "./pdfs")
    if not os.path.exists(pdf_dir):
        print(f"Warning: PDF directory '{pdf_dir}' does not exist. Please create it and place PDF files inside.")
    else:
        pdf_files = find_pdfs(pdf_dir)
        if not pdf_files:
            print(f"No PDF files found in '{pdf_dir}'.")
        else:
            print(f"Found {len(pdf_files)} PDF files in '{pdf_dir}':")
            for pdf_path in pdf_files:
                filename = os.path.basename(pdf_path)
                print(f"- pdf/{filename}")

    print("Starting MCP server...")
    mcp.run()