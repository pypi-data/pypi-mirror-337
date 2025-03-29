import pytest
import json
import time
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

from ghcopilot.api import (
    GithubCopilotClient, 
    CopilotAuthError, 
    CopilotAPIError
)

# Fixtures
@pytest.fixture
def client():
    """Create a GithubCopilotClient instance for testing."""
    return GithubCopilotClient(debug=True)

@pytest.fixture
def authenticated_client():
    """Create an authenticated GithubCopilotClient instance."""
    client = GithubCopilotClient(auth_token="test_token", debug=True)
    return client

@pytest.fixture
def mock_response():
    """Create a mock response object."""
    mock = MagicMock()
    mock.status_code = 200
    mock.raise_for_status = MagicMock()
    return mock

# Tests for initialization
def test_init():
    """Test client initialization."""
    client = GithubCopilotClient()
    assert client.auth_token is None
    assert hasattr(client, 'session')

    client = GithubCopilotClient(auth_token="test_token")
    assert client.auth_token == "test_token"

# Tests for token file operations
def test_load_token_from_file_success():
    """Test successful token loading from file."""
    current_time = int(time.time())
    mock_data = f"test_token\n{current_time - 60}"  # token created 1 minute ago
    
    with patch("builtins.open", mock_open(read_data=mock_data)):
        client = GithubCopilotClient()
        result = client.load_token_from_file()
        
        assert result is True
        assert client.auth_token == "test_token"

def test_load_token_from_file_expired():
    """Test loading expired token."""
    current_time = int(time.time())
    # Token created 31 minutes ago (default timeout is 30)
    mock_data = f"test_token\n{current_time - 31*60}"
    
    with patch("builtins.open", mock_open(read_data=mock_data)):
        client = GithubCopilotClient()
        result = client.load_token_from_file()
        
        assert result is False
        assert client.auth_token is None

def test_load_token_from_file_not_found():
    """Test loading token from non-existent file."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        client = GithubCopilotClient()
        result = client.load_token_from_file()
        
        assert result is False

def test_load_token_from_file_invalid_format():
    """Test loading token with invalid format."""
    with patch("builtins.open", mock_open(read_data="just_a_token")):
        client = GithubCopilotClient()
        result = client.load_token_from_file()
        
        assert result is False

def test_save_token_to_file():
    """Test saving token to file."""
    m = mock_open()
    with patch("builtins.open", m):
        with patch("time.time", return_value=12345):
            client = GithubCopilotClient(auth_token="test_token")
            client.save_token_to_file()
            
            m().write.assert_any_call("test_token\n12345")

def test_save_token_to_file_no_token():
    """Test saving when no token is available."""
    client = GithubCopilotClient()
    
    with pytest.raises(CopilotAuthError):
        client.save_token_to_file()

# Tests for authentication
@patch("selenium.webdriver.Chrome")
def test_get_cookies(mock_chrome):
    """Test getting cookies from browser."""
    # Setup mock driver instance
    mock_driver = MagicMock()
    mock_chrome.return_value = mock_driver
    
    # Mock cookies
    mock_cookies = [
        {"name": "cookie1", "value": "value1"},
        {"name": "cookie2", "value": "value2"}
    ]
    mock_driver.get_cookies.return_value = mock_cookies
    
    client = GithubCopilotClient()
    cookies = client.get_cookies()
    
    # Assert that driver gets called with GitHub login URL
    mock_driver.get.assert_called_once_with('https://github.com/login')
    
    # Assert cookies are formatted correctly
    assert cookies == {"cookie1": "value1", "cookie2": "value2"}
    
    # Verify driver.quit was called
    mock_driver.quit.assert_called_once()

@patch("requests.Session.post")
def test_authenticate_with_cookies(mock_post, mock_response):
    """Test authentication with provided cookies."""
    mock_response.json.return_value = {"token": "test_token"}
    mock_post.return_value = mock_response
    
    client = GithubCopilotClient()
    token = client.authenticate(cookies={"cookie1": "value1"})
    
    assert token == "test_token"
    assert client.auth_token == "test_token"
    
    # Check that the request was made to the correct URL with cookies
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert 'https://github.com/github-copilot/chat/token' in args[0]
    assert kwargs['cookies'] == {"cookie1": "value1"}

# Tests for API methods
def test_get_auth_headers():
    """Test generating authentication headers."""
    client = GithubCopilotClient()
    
    # Should raise error when no token is set
    with pytest.raises(CopilotAuthError):
        client._get_auth_headers()
    
    # Should include token when set
    client.auth_token = "test_token"
    headers = client._get_auth_headers()
    
    assert headers['authorization'] == 'GitHub-Bearer test_token'
    assert 'copilot-integration-id' in headers

@patch("requests.Session.get")
def test_get_latest_thread_success(mock_get, mock_response, authenticated_client):
    """Test getting latest thread successful."""
    mock_response.json.return_value = {"threads": [{"id": "thread_id"}]}
    mock_get.return_value = mock_response
    
    thread_id = authenticated_client.get_latest_thread()
    
    assert thread_id == "thread_id"
    mock_get.assert_called_with(
        'https://api.individual.githubcopilot.com/github/chat/threads', 
        headers=authenticated_client._get_auth_headers()
    )

@patch("requests.Session.get")
def test_get_latest_thread_empty(mock_get, mock_response, authenticated_client):
    """Test getting latest thread when no threads exist."""
    mock_response.json.return_value = {"threads": []}
    mock_get.return_value = mock_response
    
    # Mock create_new_thread method
    authenticated_client.create_new_thread = MagicMock(return_value="new_thread_id")
    
    thread_id = authenticated_client.get_latest_thread()
    
    assert thread_id == "new_thread_id"
    authenticated_client.create_new_thread.assert_called_once()

@patch("requests.Session.post")
def test_create_new_thread_success(mock_post, mock_response, authenticated_client):
    """Test creating a new thread."""
    mock_response.json.return_value = {"id": "new_thread_id"}
    mock_post.return_value = mock_response
    
    thread_id = authenticated_client.create_new_thread()
    
    assert thread_id == "new_thread_id"
    mock_post.assert_called_with(
        'https://api.individual.githubcopilot.com/github/chat/threads', 
        headers=authenticated_client._get_auth_headers(),
        json={}
    )

@patch("requests.Session.delete")
def test_delete_thread_success(mock_delete, authenticated_client):
    """Test deleting a thread successfully."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_delete.return_value = mock_response
    
    result = authenticated_client.delete_thread("thread_id")
    
    assert result is True
    mock_delete.assert_called_with(
        'https://api.individual.githubcopilot.com/github/chat/threads/thread_id',
        headers=authenticated_client._get_auth_headers()
    )

@patch("requests.Session.delete")
def test_delete_thread_failure(mock_delete, authenticated_client):
    """Test deleting a thread with error."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_delete.return_value = mock_response
    
    with pytest.raises(CopilotAPIError):
        authenticated_client.delete_thread("thread_id")

@patch("requests.Session.get")
def test_get_models_success(mock_get, mock_response, authenticated_client):
    """Test getting available models."""
    mock_response.json.return_value = {
        "data": [
            {"id": "model1", "name": "Model One"},
            {"id": "model2", "name": "Model Two"}
        ]
    }
    mock_get.return_value = mock_response
    
    models = authenticated_client.get_models()
    
    assert len(models) == 2
    assert models[0]["id"] == "model1"
    assert models[1]["name"] == "Model Two"
    mock_get.assert_called_with(
        'https://api.individual.githubcopilot.com/models', 
        headers=authenticated_client._get_auth_headers()
    )

@patch("requests.Session.post")
def test_send_message(mock_post, authenticated_client):
    """Test sending a message and getting streamed response."""
    # Mock response content
    mock_response = MagicMock()
    mock_response.iter_lines.return_value = [
        b'data: {"type":"content","body":"Hello"}',
        b'data: {"type":"content","body":" world"}',
        b'data: {"type":"complete","copilotAnnotations":{"CodeVulnerability":[],"PublicCodeReference":[{"url":"https://example.com"}]}}'
    ]
    mock_post.return_value = mock_response
    
    # Mock get_latest_thread
    authenticated_client.get_latest_thread = MagicMock(return_value="thread_id")
    
    # Collect generator results
    results = list(authenticated_client.send_message("Hi", "model1"))
    
    assert len(results) == 3
    assert results[0] == {"type": "content", "text": "Hello"}
    assert results[1] == {"type": "content", "text": " world"}
    assert results[2]["type"] == "complete"
    assert len(results[2]["references"]) == 1

@patch("requests.Session.post")
def test_get_inline_completion(mock_post, authenticated_client):
    """Test getting inline code completion."""
    mock_response = MagicMock()
    mock_response.iter_lines.return_value = [
        b'data: {"choices": [{"text": "def hello():"}]}',
        b'data: {"choices": [{"text": " print(\'world\')"}]}'
    ]
    mock_post.return_value = mock_response
    
    completion = authenticated_client.get_inline_completion("def ")
    
    assert completion == "def hello(): print('world')"
    mock_post.assert_called_once()

def test_get_inline_completion_no_auth(client):
    """Test getting inline completion without authentication."""
    with pytest.raises(CopilotAuthError):
        client.get_inline_completion("def ")
