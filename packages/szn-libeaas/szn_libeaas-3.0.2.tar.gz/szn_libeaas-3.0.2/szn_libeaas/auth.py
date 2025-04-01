"""
Authentication functionality for the szn-libeaas package.

This module provides classes for API authentication and token management.
"""
import time
import base64
import hmac
import hashlib
import threading
from typing import Dict, Optional, Any

class Authentication:
    """
    Handles API authentication.
    
    This class provides methods for generating auth headers using API keys
    or tokens.
    """
    
    def __init__(self, api_key: Optional[str] = None, token: Optional[str] = None):
        """
        Initialize authentication with either API key or token.
        
        Args:
            api_key: API key for authentication
            token: Authentication token (alternative to API key)
        """
        self.api_key = api_key
        self.token = token
        self._lock = threading.RLock()
    
    def get_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests.
        
        Returns:
            Dictionary of headers to include in API requests
        """
        with self._lock:
            headers = {}
            
            if self.token:
                headers['Authorization'] = f'Bearer {self.token}'
            elif self.api_key:
                headers['X-API-Key'] = self.api_key
            
            return headers
    
    def set_token(self, token: str) -> None:
        """
        Set the authentication token.
        
        Args:
            token: The authentication token to use
        """
        with self._lock:
            self.token = token
    
    def clear_token(self) -> None:
        """Clear the authentication token."""
        with self._lock:
            self.token = None
    
    def generate_signature(self, payload: str, timestamp: Optional[int] = None) -> Dict[str, str]:
        """
        Generate a signature for authenticated requests.
        
        Args:
            payload: The data to sign
            timestamp: Optional timestamp to use (default: current time)
            
        Returns:
            Dictionary with signature and timestamp
        """
        if not self.api_key:
            raise ValueError("API key is required for signature generation")
        
        timestamp = timestamp or int(time.time())
        
        # Create signature using HMAC-SHA256
        signature_data = f"{timestamp}.{payload}"
        signature = hmac.new(
            key=self.api_key.encode('utf-8'),
            msg=signature_data.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        return {
            'signature': signature,
            'timestamp': str(timestamp)
        }


class TokenManager:
    """
    Manages authentication tokens.
    
    This class handles token acquisition, refreshing, and caching.
    """
    
    def __init__(self, client):
        """
        Initialize the token manager.
        
        Args:
            client: API client instance
        """
        self.client = client
        self.token = None
        self.token_expires_at = 0
        self.refresh_token = None
        self._lock = threading.RLock()
    
    def get_token(self, force_refresh: bool = False) -> str:
        """
        Get a valid authentication token.
        
        Args:
            force_refresh: Force refreshing the token even if it's not expired
            
        Returns:
            Valid authentication token
        """
        with self._lock:
            now = time.time()
            
            # If token is missing or expired or forced refresh
            if force_refresh or not self.token or now >= self.token_expires_at - 300:  # Refresh 5 min before expiry
                self._refresh_token()
            
            return self.token
    
    def _refresh_token(self) -> None:
        """
        Refresh the authentication token.
        
        This method is called automatically when the token is expired.
        """
        with self._lock:
            # If we have a refresh token, use it
            if self.refresh_token:
                response = self.client.post(
                    'auth/refresh',
                    json_data={'refresh_token': self.refresh_token},
                    headers={'Authorization': None}  # Avoid using the expired token
                )
            # Otherwise get a new token with API key
            elif self.client.api_key:
                response = self.client.post(
                    'auth/token',
                    headers={'Authorization': None}  # Avoid using expired token
                )
            else:
                raise ValueError("No API key or refresh token available for authentication")
            
            # Extract token information
            self.token = response.get('access_token')
            self.refresh_token = response.get('refresh_token')
            
            # Calculate token expiry time
            expires_in = response.get('expires_in', 3600)  # Default 1 hour
            self.token_expires_at = time.time() + expires_in
            
            # Update client authentication
            self.client.auth.set_token(self.token)
    
    def clear(self) -> None:
        """Clear all token data."""
        with self._lock:
            self.token = None
            self.refresh_token = None
            self.token_expires_at = 0
            self.client.auth.clear_token()