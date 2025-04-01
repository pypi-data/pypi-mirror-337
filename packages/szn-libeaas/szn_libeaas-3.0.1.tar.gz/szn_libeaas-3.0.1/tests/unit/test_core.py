"""
Unit tests for the core module.
"""
import unittest
from unittest import mock
import json
import time
from szn_libeaas.core import Client, APIResponse, APIError


class TestAPIResponse(unittest.TestCase):
    """Tests for the APIResponse class."""
    
    def test_success_property(self):
        """Test the success property returns correct values."""
        # Success case - 200 status code
        response = APIResponse(
            status_code=200,
            data={"result": "success"},
            headers={}
        )
        self.assertTrue(response.success)
        
        # Success case - 299 status code
        response = APIResponse(
            status_code=299,
            data={"result": "success"},
            headers={}
        )
        self.assertTrue(response.success)
        
        # Failure case - 400 status code
        response = APIResponse(
            status_code=400,
            data={"error": "Bad request"},
            headers={}
        )
        self.assertFalse(response.success)
    
    def test_get_method(self):
        """Test the get method for accessing data."""
        response = APIResponse(
            status_code=200,
            data={"user": {"name": "Test User", "id": 123}},
            headers={}
        )
        
        # Test getting a value that exists
        self.assertEqual(response.get("user"), {"name": "Test User", "id": 123})
        
        # Test getting a value that doesn't exist
        self.assertIsNone(response.get("non_existent"))
        
        # Test getting a value with a default
        self.assertEqual(response.get("non_existent", "default"), "default")
        
        # Test when data is not a dictionary
        response = APIResponse(
            status_code=200,
            data=["item1", "item2"],
            headers={}
        )
        self.assertIsNone(response.get("key"))


class TestAPIError(unittest.TestCase):
    """Tests for the APIError class."""
    
    def test_initialization(self):
        """Test error initialization."""
        error = APIError(
            status_code=404,
            message="Resource not found",
            request_id="req-123"
        )
        
        self.assertEqual(error.status_code, 404)
        self.assertEqual(error.message, "Resource not found")
        self.assertEqual(error.request_id, "req-123")
        
        # Test the string representation
        self.assertIn("404", str(error))
        self.assertIn("Resource not found", str(error))
        self.assertIn("req-123", str(error))


class TestClient(unittest.TestCase):
    """Tests for the Client class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = Client(
            api_key="test_key",
            base_url="https://test.api",
            verify_ssl=False,
            debug=True
        )
    
    def test_initialization(self):
        """Test client initialization."""
        self.assertEqual(self.client.api_key, "test_key")
        self.assertEqual(self.client.base_url, "https://test.api")
        self.assertEqual(self.client.verify_ssl, False)
        self.assertEqual(self.client.debug, True)
        
        # Default values
        client = Client()
        self.assertEqual(client.base_url, Client.DEFAULT_BASE_URL)
        self.assertEqual(client.timeout, Client.DEFAULT_TIMEOUT)
        self.assertEqual(client.verify_ssl, True)
    
    @mock.patch('szn_libeaas.core.requests.Session.request')
    def test_request_success(self, mock_request):
        """Test successful API request."""
        # Mock response
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = json.dumps({"data": "test"}).encode('utf-8')
        mock_response.json.return_value = {"data": "test"}
        mock_response.headers = {'X-Request-ID': 'req-456'}
        
        mock_request.return_value = mock_response
        
        # Make the request
        response = self.client.request(
            method="GET",
            endpoint="test/endpoint",
            params={"param": "value"},
            headers={"X-Custom": "Header"}
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"data": "test"})
        self.assertEqual(response.get("data"), "test")
        self.assertTrue(response.success)
        
        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        
        self.assertEqual(kwargs['method'], 'GET')
        self.assertEqual(kwargs['url'], 'https://test.api/test/endpoint')
        self.assertEqual(kwargs['params'], {"param": "value"})
        self.assertIn('User-Agent', kwargs['headers'])
        self.assertIn('X-Custom', kwargs['headers'])
        self.assertIn('X-API-Key', kwargs['headers'])
        self.assertEqual(kwargs['headers']['X-API-Key'], 'test_key')
    
    @mock.patch('szn_libeaas.core.requests.Session.request')
    def test_request_error(self, mock_request):
        """Test API request with error response."""
        # Mock response
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_response.content = json.dumps({"error": "Not found"}).encode('utf-8')
        mock_response.json.return_value = {"error": "Not found"}
        mock_response.headers = {'X-Request-ID': 'req-789'}
        
        mock_request.return_value = mock_response
        
        # Make the request and check for exception
        with self.assertRaises(APIError) as context:
            self.client.get("test/endpoint")
        
        # Check the error details
        error = context.exception
        self.assertEqual(error.status_code, 404)
        self.assertEqual(error.message, "Not found")
        self.assertEqual(error.request_id, "req-789")
    
    @mock.patch('szn_libeaas.core.requests.Session.request')
    def test_convenience_methods(self, mock_request):
        """Test convenience methods for HTTP verbs."""
        # Mock response
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = json.dumps({"data": "test"}).encode('utf-8')
        mock_response.json.return_value = {"data": "test"}
        mock_response.headers = {}
        
        mock_request.return_value = mock_response
        
        # Test convenience methods
        self.client.get("test/get")
        self.client.post("test/post", json_data={"key": "value"})
        self.client.put("test/put", data={"key": "value"})
        self.client.delete("test/delete")
        self.client.patch("test/patch")
        
        # Check that requests were made with correct HTTP methods
        self.assertEqual(mock_request.call_count, 5)
        
        calls = mock_request.call_args_list
        self.assertEqual(calls[0][1]['method'], 'GET')
        self.assertEqual(calls[1][1]['method'], 'POST')
        self.assertEqual(calls[2][1]['method'], 'PUT')
        self.assertEqual(calls[3][1]['method'], 'DELETE')
        self.assertEqual(calls[4][1]['method'], 'PATCH')
    
    def test_context_manager(self):
        """Test client as a context manager."""
        with mock.patch.object(self.client, 'close') as mock_close:
            with self.client as client:
                self.assertEqual(client, self.client)
            
            # Check that close was called
            mock_close.assert_called_once()


if __name__ == '__main__':
    unittest.main()