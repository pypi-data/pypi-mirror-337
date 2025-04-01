"""
Core API functionality for the szn-libeaas package.

This module provides the main Client class and related response handling.
"""
import json
import time
import requests
from typing import Dict, List, Any, Optional, Union

from .auth import Authentication, TokenManager
from .utils import Logger, ConfigManager


class APIError(Exception):
    """Exception raised for API errors."""
    
    def __init__(self, status_code: int, message: str, request_id: Optional[str] = None):
        """
        Initialize API error with details.
        
        Args:
            status_code: HTTP status code of the error
            message: Error message
            request_id: Optional request ID for tracking
        """
        self.status_code = status_code
        self.message = message
        self.request_id = request_id
        super().__init__(f"API Error ({status_code}): {message} - Request ID: {request_id}")


class APIResponse:
    """Wrapper for API responses with convenient data access methods."""
    
    def __init__(self, 
                 status_code: int, 
                 data: Any, 
                 headers: Dict[str, str],
                 request_id: Optional[str] = None,
                 request_time: Optional[float] = None):
        """
        Initialize API response with data.
        
        Args:
            status_code: HTTP status code
            data: Response data (usually JSON-decoded)
            headers: Response headers
            request_id: Optional request ID for tracking
            request_time: Optional time taken for the request in seconds
        """
        self.status_code = status_code
        self.data = data
        self.headers = headers
        self.request_id = request_id or headers.get('X-Request-ID')
        self.request_time = request_time
        
    @property
    def success(self) -> bool:
        """Return True if the request was successful (2xx status code)."""
        return 200 <= self.status_code < 300
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the response data by key."""
        if isinstance(self.data, dict):
            return self.data.get(key, default)
        return default
    
    def __repr__(self) -> str:
        """String representation of the response."""
        return f"<APIResponse status={self.status_code} request_id={self.request_id}>"


class Client:
    """
    Main client for interacting with the EaaS API.
    
    This class provides the core functionality for making API requests and
    handling responses.
    """
    
    DEFAULT_TIMEOUT = 30  # seconds
    DEFAULT_BASE_URL = "https://api.szn-libeaas.com/v3"
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 timeout: Optional[int] = None,
                 verify_ssl: bool = True,
                 debug: bool = False,
                 retries: int = 3,
                 config_file: Optional[str] = None):
        """
        Initialize the API client.
        
        Args:
            api_key: API key for authentication
            base_url: Custom base URL for API endpoints
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            debug: Enable debug logging
            retries: Number of retries for failed requests
            config_file: Path to optional config file
        """
        self.config = ConfigManager(config_file=config_file)
        
        # Set configuration with priority: constructor args > config file > defaults
        self.api_key = api_key or self.config.get('api_key')
        self.base_url = base_url or self.config.get('base_url') or self.DEFAULT_BASE_URL
        self.timeout = timeout or self.config.get('timeout') or self.DEFAULT_TIMEOUT
        self.verify_ssl = self.config.get('verify_ssl', verify_ssl)
        self.debug = debug or self.config.get('debug', False)
        self.retries = retries or self.config.get('retries', 3)
        
        # Initialize components
        self.logger = Logger(debug=self.debug)
        self.auth = Authentication(api_key=self.api_key)
        self.token_manager = TokenManager(self)
        
        # Setup session
        self.session = requests.Session()
        self.session.verify = self.verify_ssl
        
        self.logger.debug(f"Client initialized: base_url={self.base_url}, timeout={self.timeout}")
    
    def request(self, 
                method: str, 
                endpoint: str, 
                params: Optional[Dict[str, Any]] = None,
                data: Optional[Dict[str, Any]] = None,
                json_data: Optional[Dict[str, Any]] = None,
                headers: Optional[Dict[str, str]] = None,
                timeout: Optional[int] = None,
                retries: Optional[int] = None) -> APIResponse:
        """
        Make an HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint (will be appended to base_url)
            params: Query parameters
            data: Form data
            json_data: JSON data (will be serialized)
            headers: Additional headers
            timeout: Custom timeout for this request
            retries: Custom retry count for this request
            
        Returns:
            APIResponse object with the response data
            
        Raises:
            APIError: If the API returns an error
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        timeout = timeout or self.timeout
        retries = retries or self.retries
        
        # Prepare headers
        request_headers = {
            'User-Agent': f'szn-libeaas-python/{__import__("szn_libeaas").__version__}',
            'Accept': 'application/json',
        }
        
        # Add auth headers
        auth_headers = self.auth.get_headers()
        request_headers.update(auth_headers)
        
        # Add custom headers
        if headers:
            request_headers.update(headers)
        
        self.logger.debug(f"Making {method} request to {url}")
        
        # For timing the request
        start_time = time.time()
        
        # Setup for retries
        attempts = 0
        last_exception = None
        
        while attempts < retries:
            attempts += 1
            try:
                response = self.session.request(
                    method=method.upper(),
                    url=url,
                    params=params,
                    data=data,
                    json=json_data,
                    headers=request_headers,
                    timeout=timeout
                )
                
                request_time = time.time() - start_time
                self.logger.debug(f"Request completed in {request_time:.3f}s with status {response.status_code}")
                
                # Parse response data
                response_data = None
                if response.content:
                    try:
                        response_data = response.json()
                    except ValueError:
                        response_data = response.text
                
                # Check for API errors
                if not (200 <= response.status_code < 300):
                    error_message = "Unknown error"
                    request_id = response.headers.get('X-Request-ID')
                    
                    if isinstance(response_data, dict):
                        error_message = response_data.get('message', response_data.get('error', error_message))
                    
                    raise APIError(
                        status_code=response.status_code,
                        message=error_message,
                        request_id=request_id
                    )
                
                # Return successful response
                return APIResponse(
                    status_code=response.status_code,
                    data=response_data,
                    headers=dict(response.headers),
                    request_time=request_time
                )
                
            except (requests.RequestException, APIError) as e:
                last_exception = e
                
                # Only retry on network errors or 5xx errors
                if isinstance(e, APIError) and e.status_code < 500:
                    raise
                
                if attempts < retries:
                    retry_delay = 2 ** attempts  # Exponential backoff
                    self.logger.debug(f"Request failed, retrying in {retry_delay}s (attempt {attempts}/{retries})")
                    time.sleep(retry_delay)
        
        # If we get here, all retries failed
        if isinstance(last_exception, APIError):
            raise last_exception
        
        raise APIError(
            status_code=500,
            message=f"Request failed after {retries} attempts: {str(last_exception)}",
            request_id=None
        )
    
    # Convenience methods for different HTTP verbs
    
    def get(self, endpoint: str, **kwargs) -> APIResponse:
        """Make a GET request."""
        return self.request('GET', endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> APIResponse:
        """Make a POST request."""
        return self.request('POST', endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> APIResponse:
        """Make a PUT request."""
        return self.request('PUT', endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> APIResponse:
        """Make a DELETE request."""
        return self.request('DELETE', endpoint, **kwargs)
    
    def patch(self, endpoint: str, **kwargs) -> APIResponse:
        """Make a PATCH request."""
        return self.request('PATCH', endpoint, **kwargs)
    
    def close(self) -> None:
        """Close the client session."""
        self.session.close()
        self.logger.debug("Client session closed")
    
    def __enter__(self):
        """Support for context manager protocol."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support for context manager protocol."""
        self.close()