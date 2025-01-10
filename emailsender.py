import os
import logging
import requests
import base64
from typing import List, Optional, Dict
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

    def _prepare_attachment(self, file_path: str, is_inline: bool = True) -> Dict:
        """Prepare file attachment for the email."""
        try:
            logger.info(f"Preparing {'inline' if is_inline else 'regular'} attachment: {file_path}")
            
            with open(file_path, 'rb') as file:
                content = file.read()
                content_b64 = base64.b64encode(content).decode('utf-8')
                
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            content_type = self._get_content_type(file_path)
            
            logger.info(f"File details - Name: {file_name}, Size: {file_size}, Type: {content_type}")
            
            attachment = {
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": file_name,
                "contentBytes": content_b64,
                "size": file_size,
                "contentType": content_type
            }
            
            if is_inline:
                attachment.update({
                    "contentId": file_name,
                    "isInline": True,
                    "contentLocation": file_name
                })
                logger.info(f"Added inline properties for {file_name}")
            
            logger.info(f"Successfully prepared attachment: {file_name}")
            return attachment
        except Exception as e:
            logger.error(f"Failed to prepare attachment {file_path}: {str(e)}")
            raise

    def _get_content_type(self, file_path: str) -> str:
        """Determine content type based on file extension."""
        ext = os.path.splitext(file_path)[1].lower()
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.mp4': 'video/mp4',
            '.mov': 'video/quicktime',
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.ppt': 'application/vnd.ms-powerpoint',
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            '.txt': 'text/plain',
            '.csv': 'text/csv',
            '.zip': 'application/zip',
            '.rar': 'application/x-rar-compressed'
        }
        return content_types.get(ext, 'application/octet-stream')  # Default to binary if unknown

    def send_email(
        self,
        to_emails: List[str],
        subject: str,
        body: str,
        embedded_media: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None,
        is_html: bool = False
    ) -> bool:
        """Send email using Microsoft Graph API with optional attachments and embedded media."""
        try:
            if not self.access_token:
                self._get_access_token()

            url = f"https://graph.microsoft.com/v1.0/users/{self.user_email}/sendMail"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }

            # Handle same sender/recipient scenario
            modified_to_emails = []
            for email in to_emails:
                if email.lower() == self.user_email.lower():
                    # Add +test suffix before the @ symbol
                    name, domain = email.split('@')
                    modified_email = f"{name}+test@{domain}"
                    modified_to_emails.append(modified_email)
                    logger.info(f"Modified recipient email from {email} to {modified_email} to avoid same sender/recipient issue")
                else:
                    modified_to_emails.append(email)

            # Log the email content for debugging
            logger.info(f"Preparing email to {modified_to_emails}")
            logger.info(f"Subject: {subject}")
            logger.info(f"HTML mode: {is_html}")
            if embedded_media:
                logger.info(f"Embedded media files: {embedded_media}")
            if attachments:
                logger.info(f"Attachment files: {attachments}")

            # Add all attachments to the email
            all_attachments = []
            
            # Add embedded media as inline attachments
            if embedded_media:
                logger.info("Processing embedded media...")
                for file_path in embedded_media:
                    if os.path.exists(file_path):
                        try:
                            attachment = self._prepare_attachment(file_path, is_inline=True)
                            all_attachments.append(attachment)
                            logger.info(f"Successfully prepared embedded media: {file_path}")
                        except Exception as e:
                            logger.error(f"Failed to prepare embedded media {file_path}: {str(e)}")
            
            # Add regular attachments
            if attachments:
                logger.info("Processing attachments...")
                for file_path in attachments:
                    if os.path.exists(file_path):
                        try:
                            attachment = self._prepare_attachment(file_path, is_inline=False)
                            all_attachments.append(attachment)
                            logger.info(f"Successfully prepared attachment: {file_path}")
                        except Exception as e:
                            logger.error(f"Failed to prepare attachment {file_path}: {str(e)}")

            # Prepare the email data
            message = {
                "subject": subject,
                "body": {
                    "contentType": "HTML" if is_html else "Text",
                    "content": body
                },
                "toRecipients": [
                    {"emailAddress": {"address": email}} for email in modified_to_emails
                ]
            }

            if all_attachments:
                message["attachments"] = all_attachments
                logger.info(f"Total attachments added to email: {len(all_attachments)}")

            email_data = {
                "message": message,
                "saveToSentItems": True
            }

            # Create a copy of email_data for logging, without the actual attachment content
            email_data_log = {
                "message": {
                    **message,
                    "attachments": [
                        {
                            **att,
                            "contentBytes": f"[BASE64 CONTENT OMITTED, size: {att['size']} bytes]"
                        } for att in message.get("attachments", [])
                    ] if "attachments" in message else []
                },
                "saveToSentItems": True
            }
            logger.info(f"Final email data structure: {email_data_log}")

            response = requests.post(
                url,
                headers=headers,
                json=email_data
            )
            response.raise_for_status()
            
            logger.info(f"Email sent successfully to {modified_to_emails}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            if isinstance(e, requests.exceptions.RequestException) and hasattr(e, 'response'):
                logger.error(f"Response status code: {e.response.status_code}")
                logger.error(f"Response content: {e.response.text}")
                logger.error(f"Request headers: {headers}")
                logger.error(f"Request URL: {url}")
            return False
