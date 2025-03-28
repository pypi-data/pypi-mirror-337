import requests
from typing import Dict, Union, Optional, List
from datetime import datetime
import json


class CloudSMSClient:
    """
    Python client for the CloudSMS API
    """

    def __init__(self, api_token: str = "", sender_id: str = ""):
        """
              Initialize the GSoftware SMS SDK

              Args:
                  api_token (str): Your API token
                  base_url (str): The base URL of the GSoftware SMS API
              """
        self.api_token = api_token
        self.sender_id = sender_id
        self.base_url = "https://cloudsms.gr"
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def get_balance(self) -> Dict[str, Union[str, float]]:
        """
        Get the current account balance

        Returns:
            dict: Response containing status and balance data
        """

        response = requests.get(
            f'{self.base_url}/api/v3/balance',
            headers=self.headers
        )
        response.raise_for_status()
        data = response.json()


        if data.get("status") == "success":
            return {
                "status": "success",
                "data": data["data"]["remaining_balance"] .replace("€", "")
            }

        return {
            "status": "error",
            "message": data.get("message", "Unknown error occurred")
        }

    def send_sms(
            self,
            recipient: Union[str, List[str]],
            message: str,
            schedule_time: Optional[datetime] = None,
            dlt_template_id: Optional[str] = None
    ) -> dict:
        """
        Send SMS to one or multiple recipients

        Args:
            recipient (Union[str, List[str]]): Single number or list of numbers (comma-separated string or list)
            sender_id (str): Sender ID (max 11 chars for alphanumeric)
            message (str): Message content
            schedule_time (Optional[datetime]): Schedule time for the message
            dlt_template_id (Optional[str]): DLT template ID for Indian SMS

        Returns:
            dict: API response
        """
        if isinstance(recipient, list):
            recipient = ','.join(recipient)

        payload = {
            'recipient': recipient,
            'sender_id': self.sender_id,
            'type': 'plain',
            'message': message
        }

        if schedule_time:
            payload['schedule_time'] = schedule_time.strftime('%Y-%m-%d %H:%M')

        if dlt_template_id:
            payload['dlt_template_id'] = dlt_template_id

        response = requests.post(
            f'{self.base_url}/api/v3/sms/send',
            headers=self.headers,
            json=payload
        )
        return response.json()

    def send_campaign(
            self,
            contact_list_ids: Union[str, List[str]],
            message: str,
            schedule_time: Optional[datetime] = None,
            dlt_template_id: Optional[str] = None
    ) -> dict:
        """
        Send SMS campaign to one or multiple contact lists

        Args:
            contact_list_ids (Union[str, List[str]]): Single contact list ID or multiple IDs
            sender_id (str): Sender ID (max 11 chars for alphanumeric)
            message (str): Message content
            schedule_time (Optional[datetime]): Schedule time for the campaign
            dlt_template_id (Optional[str]): DLT template ID for Indian SMS

        Returns:
            dict: API response
        """
        if isinstance(contact_list_ids, list):
            contact_list_ids = ','.join(contact_list_ids)

        payload = {
            'recipient': contact_list_ids,
            'sender_id': self.sender_id,
            'type': 'plain',
            'message': message
        }

        if schedule_time:
            payload['schedule_time'] = schedule_time.strftime('%Y-%m-%d %H:%M')

        if dlt_template_id:
            payload['dlt_template_id'] = dlt_template_id

        response = requests.post(
            f'{self.base_url}/api/v3/sms/campaign',
            headers=self.headers,
            json=payload
        )
        return response.json()

    def get_sms(self, uid: str) -> dict:
        """
        Get details of a specific SMS

        Args:
            uid (str): Unique ID of the SMS

        Returns:
            dict: SMS details
        """
        response = requests.get(
            f'{self.base_url}/api/v3/sms/{uid}',
            headers=self.headers
        )
        return response.json()

    def list_sms(self) -> dict:
        """
        Get list of all SMS messages

        Returns:
            dict: List of SMS messages with pagination
        """
        response = requests.get(
            f'{self.base_url}/api/v3/sms',
            headers=self.headers
        )
        return response.json()

    def get_campaign(self, uid: str) -> dict:
        """
        Get details of a specific campaign

        Args:
            uid (str): Unique ID of the campaign

        Returns:
            dict: Campaign details
        """
        response = requests.get(
            f'{self.base_url}/api/v3/campaign/{uid}',
            headers=self.headers
        )
        return response.json()
