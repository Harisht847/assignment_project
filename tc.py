import os
import pytest
from unittest.mock import Mock, patch
from main import DirectoryReader, FileTypeIdentifier, upload_to_s3, upload_to_gcs, upload_file_async

@pytest.fixture
def mock_s3_client():
    with patch('boto3.client') as mock_client:
        yield mock_client

@pytest.fixture
def directory_reader():
    return DirectoryReader('/mock/directory')

@pytest.fixture
def file_type_identifier():
    return FileTypeIdentifier()

def test_upload_to_s3(mock_s3_client):
    # Arrange
    file_path = '/mock/directory/test_file.txt'
    
    # Act
    upload_to_s3(file_path)
    
    # Assert
    mock_s3_client.return_value.upload_file.assert_called_once_with(
        file_path, 'cloudstorageappfiles', os.path.basename(file_path)
    )

def test_upload_file_async(monkeypatch, file_type_identifier):
    # Arrange
    mock_loop = Mock()
    monkeypatch.setattr(asyncio, 'get_event_loop', Mock(return_value=mock_loop))
    mock_loop.run_in_executor.return_value = None
    
    file_path = '/mock/directory/test_file.txt'

    # Act
    asyncio.run(upload_file_async(file_path, file_type_identifier))

    # Assert
    assert mock_loop.run_in_executor.called

def test_upload_file_async_with_logger(monkeypatch, caplog, file_type_identifier):
    # Arrange
    mock_loop = Mock()
    monkeypatch.setattr(asyncio, 'get_event_loop', Mock(return_value=mock_loop))
    mock_loop.run_in_executor.return_value = None
    
    file_path = '/mock/directory/test_file.txt'

    # Act
    asyncio.run(upload_file_async(file_path, file_type_identifier))

    # Assert
    assert mock_loop.run_in_executor.called
    assert caplog.records[0].message == f'File "{file_path}" has been uploaded asynchronously to S3.'
