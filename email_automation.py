from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import pandas as pd
from pathlib import Path
import json
import logging
from datetime import datetime
import asyncio
from email_validator import validate_email, EmailNotValidError
from string import Template
import os
from dotenv import load_dotenv
from emailsender import EmailSender

@dataclass
class EmailConfig:
    """Configuration settings for email automation."""
    template_path: str
    email_subject: str
    sender_info: Dict[str, str]
    email_settings: Dict[str, int]

    @property
    def max_retries(self) -> int:
        return self.email_settings.get('max_retries', 3)
    
    @property
    def batch_size(self) -> int:
        return self.email_settings.get('batch_size', 50)
    
    @property
    def rate_limit(self) -> int:
        return self.email_settings.get('rate_limit', 100)

class EmailTemplate:
    """Handles email template loading and personalization."""
    def __init__(self, template_path: str) -> None:
        self.template: Optional[Template] = None
        self.template_path = Path(template_path)
        self._last_modified: float = 0
        self._load_template()

    def _load_template(self) -> None:
        """Load template from file, with caching based on modification time."""
        current_mtime = os.path.getmtime(self.template_path)
        if current_mtime > self._last_modified:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                self.template = Template(f.read())
            self._last_modified = current_mtime

    def personalize(self, data: Dict[str, Any]) -> str:
        """Create personalized email content from template and data."""
        self._load_template()  # Reload if template has changed
        if not self.template:
            raise ValueError("Template not loaded")
        
        # Convert all values to strings to avoid type issues
        safe_data = {k: str(v) if v is not None else '' for k, v in data.items()}
        return self.template.safe_substitute(safe_data)

class EmailCampaign:
    def __init__(self, config_path: str):
        self.logger = self._setup_logging()
        self.config = self._load_config(config_path)
        self.email_sender = EmailSender()
        self.template = EmailTemplate(self.config.template_path)

    @staticmethod
    def _setup_logging() -> logging.Logger:
        """Configure logging with rotation."""
        log_path = Path('logs')
        log_path.mkdir(exist_ok=True)
        
        logging.basicConfig(
            filename=log_path / f'email_campaign_{datetime.now().strftime("%Y%m%d")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger('EmailCampaign')

    def _load_config(self, config_path: str) -> EmailConfig:
        """Load and validate configuration."""
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            return EmailConfig(**config_data)
        except Exception as e:
            self.logger.error(f"Configuration error: {str(e)}")
            raise

    async def process_contacts(self, contacts_file: str) -> Dict[str, int]:
        """Process contacts from Excel/CSV file and send emails."""
        results = {'total': 0, 'successful': 0, 'failed': 0, 'skipped': 0}
        
        try:
            # Read the contacts file
            df = pd.read_excel(contacts_file) if contacts_file.endswith(('.xlsx', '.xls')) \
                else pd.read_csv(contacts_file)
            
            # Only process contacts with pending status
            pending_contacts = df[df['status'].str.lower() == 'pending'].copy()
            results['skipped'] = len(df) - len(pending_contacts)
            
            for batch_start in range(0, len(pending_contacts), self.config.batch_size):
                batch = pending_contacts.iloc[batch_start:batch_start + self.config.batch_size]
                
                for idx, row in batch.iterrows():
                    try:
                        # Validate email
                        validate_email(row['email'])
                        
                        # Combine contact data with sender info
                        template_data = {**row.to_dict(), **self.config.sender_info}
                        
                        # Personalize content
                        content = self.template.personalize(template_data)
                        subject = self.config.email_subject.format(**template_data)
                        
                        # Log the content for debugging
                        self.logger.info(f"Prepared email content for {row['email']}:\n{content}")
                        
                        # Send email
                        is_sent = self.email_sender.send_email(
                            [row['email']],
                            subject,
                            content,
                            is_html=True
                        )
                        
                        results['total'] += 1
                        if is_sent:
                            results['successful'] += 1
                            self.logger.info(f"Successfully sent email to {row['email']}")
                            # Update status in the dataframe
                            df.loc[idx, 'status'] = 'sent'
                            df.loc[idx, 'email_sent_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            results['failed'] += 1
                            self.logger.error(f"Failed to send email to {row['email']}")
                            df.loc[idx, 'status'] = 'failed'
                            
                    except (EmailNotValidError, KeyError, Exception) as e:
                        self.logger.error(f"Error processing {row.get('email', 'unknown')}: {str(e)}")
                        results['failed'] += 1
                        results['total'] += 1
                        df.loc[idx, 'status'] = 'failed'
                
                # Save the updated status after each batch
                if contacts_file.endswith(('.xlsx', '.xls')):
                    df.to_excel(contacts_file, index=False)
                else:
                    df.to_csv(contacts_file, index=False)
                
                # Rate limiting
                await asyncio.sleep(60 / self.config.rate_limit * len(batch))
                
        except Exception as e:
            self.logger.error(f"Campaign error: {str(e)}")
            raise
            
        return results

async def main():
    # Example usage
    campaign = EmailCampaign('config.json')
    results = await campaign.process_contacts('contacts.xlsx')
    
    print("\nCampaign Results:")
    print(f"Total emails attempted: {results['total']}")
    print(f"Successfully sent: {results['successful']}")
    print(f"Failed: {results['failed']}")
    print(f"Skipped (already sent): {results['skipped']}")

if __name__ == "__main__":
    asyncio.run(main()) 