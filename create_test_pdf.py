
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_pdf(path: str, content: str):
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, content)
    c.save()

if __name__ == "__main__":
    # テストデータディレクトリをクリーンアップ
    if os.path.exists("/workspaces/mcp_client/pdfs"):
        for root, dirs, files in os.walk("/workspaces/mcp_client/pdfs", topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    else:
        os.makedirs("/workspaces/mcp_client/pdfs")

    # ルートディレクトリにPDFを作成
    create_pdf("/workspaces/mcp_client/pdfs/test_document.pdf", "This is a test PDF document.")
    create_pdf("/workspaces/mcp_client/pdfs/another_document.pdf", "This is another test file.")
    with open("/workspaces/mcp_client/pdfs/not_a_pdf.txt", "w") as f:
        f.write("This is a text file.")

    # サブディレクトリを作成し、PDFを作成
    os.makedirs("/workspaces/mcp_client/pdfs/subdir", exist_ok=True)
    create_pdf("/workspaces/mcp_client/pdfs/subdir/sub_document.pdf", "This is a document in a subdirectory.")
