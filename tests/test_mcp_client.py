import os
from unittest.mock import MagicMock, patch
from src.main import start_client

TEST_DATA_DIR = "/workspaces/mcp_client/tests/test_data"

@patch("src.main.Client")
@patch("src.main.find_pdfs")
@patch("src.main.extract_text_from_pdf")
def test_start_client_creates_resources(mock_extract_text_from_pdf, mock_find_pdfs, MockClient):
    """クライアントがPDFからリソースを作成することをテストします。"""
    # Arrange
    mock_find_pdfs.return_value = [
        os.path.join(TEST_DATA_DIR, "test_document.pdf"),
        os.path.join(TEST_DATA_DIR, "another_document.pdf")
    ]
    mock_extract_text_from_pdf.side_effect = [
        "This is a test PDF document.",
        "This is another test file."
    ]
    mock_client_instance = MockClient.return_value
    mock_client_instance.set_resource = MagicMock()
    mock_client_instance.get_resources = MagicMock(return_value=["pdf/test_document.pdf", "pdf/another_document.pdf"])

    # Act
    start_client(TEST_DATA_DIR)

    # Assert
    mock_find_pdfs.assert_called_once_with(TEST_DATA_DIR)
    assert mock_extract_text_from_pdf.call_count == 2
    assert mock_client_instance.set_resource.call_count == 2

    # Check the calls to set_resource
    calls = mock_client_instance.set_resource.call_args_list
    expected_calls = {
        f"pdf/test_document.pdf": "This is a test PDF document.",
        f"pdf/another_document.pdf": "This is another test file."
    }

    for call in calls:
        resource_id, content = call.args
        assert resource_id in expected_calls
        assert expected_calls[resource_id] in content
        del expected_calls[resource_id]
    
    assert not expected_calls, f"Missing calls for: {expected_calls.keys()}"

@patch("src.main.Client")
@patch("src.main.find_pdfs")
def test_start_client_no_pdfs(mock_find_pdfs, MockClient):
    """PDFが見つからない場合の動作をテストします。"""
    # Arrange
    mock_find_pdfs.return_value = []
    mock_client_instance = MockClient.return_value
    mock_client_instance.set_resource = MagicMock()

    # Act
    start_client("/tmp")

    # Assert
    mock_find_pdfs.assert_called_once_with("/tmp")
    mock_client_instance.set_resource.assert_not_called()