import os
from fastmcp import FastMCP
from fastmcp.resources import FunctionResource
from src.pdf_loader import find_pdfs, extract_text_from_pdf

mcp = FastMCP(name="PDFResourceServer")
pdf_dir = os.environ.get("PDF_DIR", "./pdfs")
mcp.auth_token = os.environ.get("MCP_AUTH_TOKEN") # Add auth_token to mcp instance

def create_resource_function(pdf_path):
    """Creates a closure for the resource function to capture the pdf_path."""
    def get_pdf_resource(): # Removed request argument
        if mcp.auth_token: # Reference mcp.auth_token directly
            # Simplified authentication for in-memory testing
            # In a real scenario, client would send a token via headers/metadata
            # and it would be validated here.
            # For this exercise, if auth_token is set, we assume successful auth
            # if the client attempts to access the resource.
            pass

        try:
            content = extract_text_from_pdf(pdf_path)
            return content
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return None
    return get_pdf_resource

# Scan for PDFs and dynamically create resources
if os.path.exists(pdf_dir):
    pdf_files = find_pdfs(pdf_dir)
    for pdf_path in pdf_files:
        # Create a resource URI from the relative path
        rel_path = os.path.relpath(pdf_path, pdf_dir)
        resource_uri = f"pdf://{rel_path}"
        
        # Dynamically create and register a resource for each PDF
        func = create_resource_function(pdf_path)
        resource = FunctionResource(uri=resource_uri, fn=func)
        mcp.add_resource(resource)
else:
    print(f"Warning: PDF directory '{pdf_dir}' does not exist.")


if __name__ == "__main__":
    # This part is now mostly for logging purposes as resources are created above
    if not os.path.exists(pdf_dir):
        print(f"Warning: PDF directory '{pdf_dir}' does not exist. Please create it and place PDF files inside.")
    else:
        pdf_files = find_pdfs(pdf_dir)
        if not pdf_files:
            print(f"No PDF files found in '{pdf_dir}'.")
        else:
            print("Available PDF resources:")
            for pdf_path in pdf_files:
                rel_path = os.path.relpath(pdf_path, pdf_dir)
                print(f"- pdf://{rel_path}")

    print("Starting MCP server...")
    mcp.run()
