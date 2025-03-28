
import requests
import json
from typing import Dict, Any, Optional

class UdeneError(Exception):
    """Base exception for Udene SDK errors"""
    pass

class RateLimitError(UdeneError):
    """Exception raised when API rate limit is exceeded"""
    def __init__(self, message: str, retry_after: int):
        self.retry_after = retry_after
        super().__init__(message)

class APIError(UdeneError):
    """Exception raised for API errors"""
    def __init__(self, message: str, status_code: int, response: Dict[str, Any]):
        self.status_code = status_code
        self.response = response
        super().__init__(message)

class UdeneClient:
    """
    Client for the Udene Fraud Detection API
    
    Args:
        api_key (str): Your Udene API key
        base_url (str, optional): Custom API base URL. Defaults to 'https://udene.net/v1'.
    """
    
    def __init__(self, api_key: str, base_url: str = 'https://udene.net/v1'):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-Client-Version': '1.0.0',
            'X-SDK-Type': 'python'
        }
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Process the API response and handle errors"""
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            raise RateLimitError(f"Rate limit exceeded. Retry after {retry_after} seconds", retry_after)
        
        if response.status_code >= 400:
            try:
                error_data = response.json()
            except ValueError:
                error_data = {"error": response.text}
            
            raise APIError(
                f"API error: {error_data.get('error', 'Unknown error')}",
                response.status_code,
                error_data
            )
        
        try:
            return response.json()
        except ValueError:
            raise UdeneError("Invalid JSON response from API")
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get fraud metrics
        
        Returns:
            Dict[str, Any]: Fraud metrics data
        """
        response = requests.get(
            f'{self.base_url}/metrics',
            headers=self.headers
        )
        return self._handle_response(response)
    
    def get_activity(self) -> Dict[str, Any]:
        """
        Get activity data
        
        Returns:
            Dict[str, Any]: Activity data
        """
        response = requests.get(
            f'{self.base_url}/activity',
            headers=self.headers
        )
        return self._handle_response(response)
    
    def track_interaction(self, **data) -> Dict[str, Any]:
        """
        Track a user interaction
        
        Args:
            **data: Interaction data key-value pairs
        
        Returns:
            Dict[str, Any]: Interaction tracking confirmation
        """
        response = requests.post(
            f'{self.base_url}/track',
            headers=self.headers,
            json=data
        )
        return self._handle_response(response)
    
    def analyze_transaction(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a transaction for fraud
        
        Args:
            transaction_data (Dict[str, Any]): Transaction data
        
        Returns:
            Dict[str, Any]: Transaction analysis results
        """
        response = requests.post(
            f'{self.base_url}/analyze-transaction',
            headers=self.headers,
            json=transaction_data
        )
        return self._handle_response(response)
