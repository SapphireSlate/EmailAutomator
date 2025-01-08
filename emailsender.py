import os
import logging
import requests
from typing import List
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.tenant_id = os.getenv('TENANT_ID')
        self.user_email = os.getenv('USER_EMAIL')
        self.access_token = None
        
    def _get_access_token(self) -> str:
        """Get Microsoft Graph API access token."""
        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'https://graph.microsoft.com/.default'
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            logger.info(f"Requesting token with client_id: {self.client_id[:8]}...")
            logger.info(f"Using tenant ID: {self.tenant_id}")
            logger.info("Making token request...")
            
            response = requests.post(url, data=data, headers=headers)
            
            if not response.ok:
                error_data = response.json()
                logger.error(f"Full token error response: {error_data}")
                logger.error(f"Request URL: {url}")
                logger.error(f"Request data: {data}")
                response.raise_for_status()
            
            token_data = response.json()
            logger.info("Token response received")
            
            if 'access_token' not in token_data:
                logger.error(f"Token response: {token_data}")
                raise ValueError("No access token in response")
            
            logger.info("Successfully obtained access token")
            self.access_token = token_data['access_token']
            return self.access_token
        except Exception as e:
            logger.error(f"Token error details: {str(e)}")
            raise

    def send_email(
        self,
        to_emails: List[str],
        subject: str,
        body: str,
        is_html: bool = False
    ) -> bool:
        """Send email using Microsoft Graph API."""
        try:
            if not self.access_token:
                self._get_access_token()

            url = f"https://graph.microsoft.com/v1.0/users/{self.user_email}/sendMail"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }

            email_data = {
                "message": {
                    "subject": subject,
                    "body": {
                        "contentType": "HTML" if is_html else "Text",
                        "content": body
                    },
                    "toRecipients": [
                        {"emailAddress": {"address": email}} for email in to_emails
                    ],
                    "from": {
                        "emailAddress": {
                            "address": self.user_email
                        }
                    }
                },
                "saveToSentItems": "true"
            }

            response = requests.post(
                url,
                headers=headers,
                json=email_data
            )
            response.raise_for_status()
            
            logger.info(f"Email sent successfully to {to_emails}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
