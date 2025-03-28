"""
CloudSMS Python SDK
~~~~~~~~~~~~~~~~~~

A Python SDK for the CloudSMS API.

Basic usage:

    >>> from cloudsms import CloudSMSClient
    >>> client = CloudSMSClient(api_token="your-token", sender_id="your-sender-id")
    >>> response = client.send_sms("+1234567890", "Hello from CloudSMS!")
    >>> print(response["status"])
    'success'

For more information, see https://cloudsms.gr/api/v3/
"""

from .client import CloudSMSClient

__version__ = "1.0.0"
__all__ = ["CloudSMSClient"]
