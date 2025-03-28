import requests
from typing import Dict, Union, Optional

class CloudSMSClient:
    """
    Python client for the CloudSMS API
    """
    
    def __init__(self, api_token: str = "", sender_id: str = ""):
        """
        Initialize the CloudSMS client
        
        Args:
            api_token (str): Your CloudSMS API token
            sender_id (str): Your CloudSMS sender ID
        """
        self.api_token = api_token
        self.sender_id = sender_id
        self.api_base_url = "https://cloudsms.gr/api/v3/"
        
    def _get_headers(self) -> Dict[str, str]:
        """Get the default headers for API requests"""
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
    def get_balance(self) -> Dict[str, Union[str, float]]:
        """
        Get the current account balance
        
        Returns:
            dict: Response containing status and balance data
        """
        if not self.api_token:
            return {
                "status": "error",
                "message": "API Token is not configured"
            }
            
        try:
            response = requests.get(
                f"{self.api_base_url}balance",
                headers=self._get_headers(),
                timeout=15
            )
            
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "success":
                return {
                    "status": "success",
                    "data": data["data"].replace("€", "")
                }
                
            return {
                "status": "error",
                "message": data.get("message", "Unknown error occurred")
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def test_connection(self) -> Dict[str, str]:
        """
        Test the API connection
        
        Returns:
            dict: Response containing status and message
        """
        if not self.api_token:
            return {
                "status": "error",
                "message": "API Token is not configured"
            }
            
        try:
            balance = self.get_balance()
            
            if balance["status"] == "success":
                return {
                    "status": "success",
                    "message": "Connection successful! Your account is properly configured."
                }
                
            return {
                "status": "error",
                "message": balance.get("message", "Unable to connect to CloudSMS API")
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def send_sms(self, phone_number: str, message: str) -> Dict[str, Union[str, bool]]:
        """
        Send an SMS message
        
        Args:
            phone_number (str): The recipient's phone number
            message (str): The message content
            
        Returns:
            dict: Response containing status and success boolean
        """
        if not self.api_token or not self.sender_id:
            return {
                "status": "error",
                "message": "API Token or Sender ID is not configured"
            }
            
        try:
            response = requests.post(
                f"{self.api_base_url}sms/send",
                headers=self._get_headers(),
                json={
                    "recipient": phone_number,
                    "sender_id": self.sender_id,
                    "type": "plain",
                    "message": message
                },
                timeout=15
            )
            
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "success":
                return {
                    "status": "success",
                    "success": True
                }
                
            return {
                "status": "error",
                "message": data.get("message", "Failed to send SMS"),
                "success": False
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": str(e),
                "success": False
            }
