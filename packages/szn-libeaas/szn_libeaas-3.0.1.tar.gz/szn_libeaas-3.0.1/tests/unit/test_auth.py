"""
Unit tests for the auth module.
"""
import unittest
from unittest import mock
import time
import hmac
import hashlib
from szn_libeaas.auth import Authentication, TokenManager


class TestAuthentication(unittest.TestCase):
    """Tests for the Authentication class."""
    
    def test_initialization(self):
        """Test initialization with different parameters."""
        # With API key
        auth = Authentication(api_key="test_key")
        self.assertEqual(auth.api_key, "test_key")
        self.assertIsNone(auth.token)
        
        # With token
        auth = Authentication(token="test_token")
        self.assertIsNone(auth.api_key)
        self.assertEqual(auth.token, "test_token")
        
        # With both
        auth = Authentication(api_key="test_key", token="test_token")
        self.assertEqual(auth.api_key, "test_key")
        self.assertEqual(auth.token, "test_token")
    
    def test_get_headers(self):
        """Test the get_headers method."""
        # With API key
        auth = Authentication(api_key="test_key")
        headers = auth.get_headers()
        self.assertEqual(headers, {"X-API-Key": "test_key"})
        
        # With token
        auth = Authentication(token="test_token")
        headers = auth.get_headers()
        self.assertEqual(headers, {"Authorization": "Bearer test_token"})
        
        # With both (token takes precedence)
        auth = Authentication(api_key="test_key", token="test_token")
        headers = auth.get_headers()
        self.assertEqual(headers, {"Authorization": "Bearer test_token"})
        
        # With neither
        auth = Authentication()
        headers = auth.get_headers()
        self.assertEqual(headers, {})
    
    def test_set_token(self):
        """Test setting a token."""
        auth = Authentication(api_key="test_key")
        self.assertIsNone(auth.token)
        
        auth.set_token("new_token")
        self.assertEqual(auth.token, "new_token")
        
        # Check that headers now use the token
        headers = auth.get_headers()
        self.assertEqual(headers, {"Authorization": "Bearer new_token"})
    
    def test_clear_token(self):
        """Test clearing a token."""
        auth = Authentication(token="test_token")
        self.assertEqual(auth.token, "test_token")
        
        auth.clear_token()
        self.assertIsNone(auth.token)
        
        # Check that headers no longer include the token
        headers = auth.get_headers()
        self.assertEqual(headers, {})
    
    def test_generate_signature(self):
        """Test signature generation."""
        auth = Authentication(api_key="test_key")
        
        # Test with fixed timestamp for deterministic result
        fixed_timestamp = 1617217200  # 2021-04-01 00:00:00 UTC
        result = auth.generate_signature("test_payload", timestamp=fixed_timestamp)
        
        # Verify the result
        self.assertIn("signature", result)
        self.assertIn("timestamp", result)
        self.assertEqual(result["timestamp"], str(fixed_timestamp))
        
        # Verify the signature is correct
        expected_signature_data = f"{fixed_timestamp}.test_payload"
        expected_signature = hmac.new(
            key="test_key".encode('utf-8'),
            msg=expected_signature_data.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        self.assertEqual(result["signature"], expected_signature)
        
        # Test without API key
        auth = Authentication()
        with self.assertRaises(ValueError):
            auth.generate_signature("test_payload")


class TestTokenManager(unittest.TestCase):
    """Tests for the TokenManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = mock.Mock()
        self.mock_client.api_key = "test_key"
        self.mock_client.auth = Authentication(api_key="test_key")
        
        self.token_manager = TokenManager(self.mock_client)
    
    def test_initialization(self):
        """Test token manager initialization."""
        self.assertEqual(self.token_manager.client, self.mock_client)
        self.assertIsNone(self.token_manager.token)
        self.assertEqual(self.token_manager.token_expires_at, 0)
        self.assertIsNone(self.token_manager.refresh_token)
    
    def test_get_token_new(self):
        """Test getting a new token when none exists."""
        # Mock the client post method to return a token
        mock_response = mock.Mock()
        mock_response.get.side_effect = lambda k, d=None: {
            "access_token": "new_token",
            "refresh_token": "refresh_token",
            "expires_in": 3600
        }.get(k, d)
        
        self.mock_client.post.return_value = mock_response
        
        # Get the token
        token = self.token_manager.get_token()
        
        # Check that the token was fetched and stored
        self.assertEqual(token, "new_token")
        self.assertEqual(self.token_manager.token, "new_token")
        self.assertEqual(self.token_manager.refresh_token, "refresh_token")
        self.assertGreater(self.token_manager.token_expires_at, time.time())
        
        # Check that the client auth was updated
        self.mock_client.auth.set_token.assert_called_with("new_token")
        
        # Check that the right endpoint was called
        self.mock_client.post.assert_called_with(
            'auth/token',
            headers={'Authorization': None}
        )
    
    def test_get_token_cached(self):
        """Test getting a cached token."""
        # Set up a valid token
        self.token_manager.token = "existing_token"
        self.token_manager.token_expires_at = time.time() + 1800  # 30 minutes from now
        
        # Get the token
        token = self.token_manager.get_token()
        
        # Check that no new token was fetched
        self.assertEqual(token, "existing_token")
        self.mock_client.post.assert_not_called()
    
    def test_get_token_expired(self):
        """Test getting a token when the current one is expired."""
        # Set up an expired token
        self.token_manager.token = "expired_token"
        self.token_manager.token_expires_at = time.time() - 60  # 1 minute ago
        self.token_manager.refresh_token = "refresh_token"
        
        # Mock the client post method to return a new token
        mock_response = mock.Mock()
        mock_response.get.side_effect = lambda k, d=None: {
            "access_token": "new_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 3600
        }.get(k, d)
        
        self.mock_client.post.return_value = mock_response
        
        # Get the token
        token = self.token_manager.get_token()
        
        # Check that a new token was fetched
        self.assertEqual(token, "new_token")
        self.assertEqual(self.token_manager.token, "new_token")
        self.assertEqual(self.token_manager.refresh_token, "new_refresh_token")
        
        # Check that the refresh endpoint was called
        self.mock_client.post.assert_called_with(
            'auth/refresh',
            json_data={'refresh_token': 'refresh_token'},
            headers={'Authorization': None}
        )
    
    def test_get_token_force_refresh(self):
        """Test force refreshing a token."""
        # Set up a valid token
        self.token_manager.token = "existing_token"
        self.token_manager.token_expires_at = time.time() + 1800  # 30 minutes from now
        self.token_manager.refresh_token = "refresh_token"
        
        # Mock the client post method to return a new token
        mock_response = mock.Mock()
        mock_response.get.side_effect = lambda k, d=None: {
            "access_token": "new_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 3600
        }.get(k, d)
        
        self.mock_client.post.return_value = mock_response
        
        # Force refresh the token
        token = self.token_manager.get_token(force_refresh=True)
        
        # Check that a new token was fetched
        self.assertEqual(token, "new_token")
        self.assertEqual(self.token_manager.token, "new_token")
        
        # Check that the refresh endpoint was called
        self.mock_client.post.assert_called_with(
            'auth/refresh',
            json_data={'refresh_token': 'refresh_token'},
            headers={'Authorization': None}
        )
    
    def test_clear(self):
        """Test clearing token data."""
        # Set up token data
        self.token_manager.token = "test_token"
        self.token_manager.refresh_token = "refresh_token"
        self.token_manager.token_expires_at = time.time() + 3600
        
        # Clear the data
        self.token_manager.clear()
        
        # Check that everything was cleared
        self.assertIsNone(self.token_manager.token)
        self.assertIsNone(self.token_manager.refresh_token)
        self.assertEqual(self.token_manager.token_expires_at, 0)
        
        # Check that the client auth was updated
        self.mock_client.auth.clear_token.assert_called_once()


if __name__ == '__main__':
    unittest.main()