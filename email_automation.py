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
    max_retries: int = 3
    batch_size: int = 50
    rate_limit: int = 100  # emails per minute

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
        return self.template.substitute(data)

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
        results = {'total': 0, 'successful': 0, 'failed': 0}
        
        try:
            df = pd.read_excel(contacts_file) if contacts_file.endswith(('.xlsx', '.xls')) \
                else pd.read_csv(contacts_file)
            
            for batch_start in range(0, len(df), self.config.batch_size):
                batch = df.iloc[batch_start:batch_start + self.config.batch_size]
                
                for _, row in batch.iterrows():
                    try:
                        # Validate email
                        validate_email(row['email'])
                        
                        # Personalize content
                        content = self.template.personalize(row.to_dict())
                        subject = self.config.email_subject.format(**row.to_dict())
                        
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
                        else:
                            results['failed'] += 1
                            
                    except (EmailNotValidError, KeyError, Exception) as e:
                        self.logger.error(f"Error processing {row.get('email', 'unknown')}: {str(e)}")
                        results['failed'] += 1
                        results['total'] += 1
                
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

if __name__ == "__main__":
    asyncio.run(main()) 