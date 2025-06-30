import os
import typer
from fastmcp.client import Client
from src.pdf_loader import find_pdfs, extract_text_from_pdf

app = typer.Typer()

@app.command()
def start_client(pdf_dir: str):
    """MCPクライアントを起動し、PDFをリソースとして公開します。"""
    client = Client()

    pdf_files = find_pdfs(pdf_dir)
    if not pdf_files:
        print(f"No PDF files found in {pdf_dir}")
        return

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        resource_id = f"pdf/{filename}"
        
        print(f"Processing {pdf_path}...")
        try:
            content = extract_text_from_pdf(pdf_path)
            if content:
                client.set_resource(resource_id, content)
                print(f"Resource '{resource_id}' created.")
            else:
                print(f"No text could be extracted from {pdf_path}.")
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")

    print("\nMCP client is running with the loaded PDF resources.")
    # 実際のシナリオでは、クライアントはアクティブになり、リクエストを待機します。
    # この例では、リソースを出力して終了します。
    # クライアントを実行し続けるには、通常、サーバープロセスでこれを実行します。
    print("\nAvailable resources:")
    for resource_id in client.get_resources():
        print(f"- {resource_id}")

if __name__ == "__main__":
    app()


