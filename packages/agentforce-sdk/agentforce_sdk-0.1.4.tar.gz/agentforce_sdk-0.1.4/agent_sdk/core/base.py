"""Base classes for the Agentforce SDK."""

import os
import json
import requests
from simple_salesforce import Salesforce, SalesforceLogin

class AgentforceBase:
    """Base class for Agentforce SDK."""
    
    API_VERSION = 'v63.0'
    
    def __init__(self, username=None, password=None, domain='login'):
        """Initialize the Agentforce SDK.
        
        Args:
            username (str): Salesforce username
            password (str): Salesforce password
            domain (str): Salesforce domain ('login' for production, 'test' for sandbox)
        """
        self.username = username
        self.password = password
        self.domain = domain
        self.session_id = None
        self.instance_url = None
        self._sf = None
        
        if username and password:
            self.login()
    
    def login(self):
        """Log in to Salesforce and get session ID and instance URL."""
        try:
            session_id, instance = SalesforceLogin(
                username=self.username, 
                password=self.password, 
                domain=self.domain
            )
            self.session_id = session_id
            self.instance_url = f"https://{instance}"
            self._sf = Salesforce(
                instance=instance, 
                session_id=session_id, 
                version=self.API_VERSION.lstrip('v')
            )
            return True
        except Exception as e:
            print(f"Error logging in to Salesforce: {e}")
            return False
    
    @property
    def sf(self):
        """Get the Salesforce connection. Login if necessary."""
        if not self._sf and self.username and self.password:
            self.login()
        return self._sf
    
    def _check_auth(self):
        """Check if authenticated to Salesforce."""
        if not self.session_id or not self.instance_url:
            raise ValueError("Not authenticated to Salesforce. Call login() first.")
    
    def execute_rest_request(self, method, endpoint, **kwargs):
        """Execute a REST request to Salesforce.
        
        Args:
            method (str): HTTP method (GET, POST, PATCH, DELETE)
            endpoint (str): API endpoint
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            dict: Response from Salesforce
        """
        self._check_auth()
        
        headers = kwargs.pop('headers', {})
        headers.update({
            'Authorization': f'Bearer {self.session_id}',
            'Content-Type': 'application/json'
        })
        
        url = f"{self.instance_url}/services/data/{self.API_VERSION}/{endpoint}"
        response = requests.request(method, url, headers=headers, **kwargs)
        
        try:
            response.raise_for_status()
            return response.json() if response.text else {}
        except requests.exceptions.HTTPError as e:
            error_message = f"HTTP Error: {e}"
            try:
                error_details = response.json()
                error_message = f"{error_message} - {json.dumps(error_details)}"
            except:
                pass
            raise ValueError(error_message)
    
    def get(self, endpoint, **kwargs):
        """Execute a GET request to Salesforce.
        
        Args:
            endpoint (str): API endpoint
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            dict: Response from Salesforce
        """
        return self.execute_rest_request('GET', endpoint, **kwargs)
    
    def post(self, endpoint, data=None, **kwargs):
        """Execute a POST request to Salesforce.
        
        Args:
            endpoint (str): API endpoint
            data (dict): Data to send in the request
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            dict: Response from Salesforce
        """
        return self.execute_rest_request('POST', endpoint, json=data, **kwargs)
    
    def patch(self, endpoint, data=None, **kwargs):
        """Execute a PATCH request to Salesforce.
        
        Args:
            endpoint (str): API endpoint
            data (dict): Data to send in the request
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            dict: Response from Salesforce
        """
        return self.execute_rest_request('PATCH', endpoint, json=data, **kwargs)
    
    def delete(self, endpoint, **kwargs):
        """Execute a DELETE request to Salesforce.
        
        Args:
            endpoint (str): API endpoint
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            dict: Response from Salesforce
        """
        return self.execute_rest_request('DELETE', endpoint, **kwargs) 