# Email Automator

An automated email sending system built with Python and Microsoft Graph API. This application allows for automated email campaigns with customizable templates, embedded images, attachments, and contact management.

## Features

- HTML email template support with embedded images
- Support for file attachments
- Contact management with Excel/CSV files
- Batch processing with rate limiting
- Detailed logging
- Customizable sender information
- Template variable substitution

## Prerequisites

- Python 3.8 or higher
- Microsoft 365 account
- Azure Account with registered application
- Required Python packages (see requirements.txt)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd EmailAutomator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Azure Application**
   1. Go to [Azure Portal](https://portal.azure.com)
   2. Register a new application
   3. Add Microsoft Graph API permissions:
      - Mail.Send
      - Mail.ReadWrite
   4. Grant admin consent for the permissions
   5. Create a new client secret
   6. Note down:
      - Client ID
      - Client Secret
      - Tenant ID

4. **Set up configuration files**
   1. Copy example files and rename:
      ```bash
      cp .env.example .env
      cp config.example.json config.json
      ```
   2. Edit `.env` with your Azure credentials:
      ```
      CLIENT_ID=your_client_id
      CLIENT_SECRET=your_client_secret
      TENANT_ID=your_tenant_id
      USER_EMAIL=your_email@domain.com
      ```
   3. Edit `config.json` with your sender information:
      ```json
      {
          "sender_info": {
              "sender_name": "Your Name",
              "sender_title": "Your Title",
              "company_name": "Your Company"
          }
      }
      ```

5. **Create required directories**
   ```bash
   mkdir -p media/embeds media/attachments logs
   ```

## Usage

1. **Prepare your media files**
   - Place embedded images in `media/embeds/`
   - Place attachments in `media/attachments/`

2. **Create contacts file**
   Run the contact creation script:
   ```bash
   python create_contacts.py
   ```
   This will create a `contacts.xlsx` file with example data. Edit this file with your actual contacts.

   Required columns:
   - email: Recipient email address
   - first_name: Recipient's first name
   - last_name: Recipient's last name
   - custom_message: Personalized message for the recipient
   - embedded_media: Semicolon-separated list of embedded image paths (optional)
   - attachments: Semicolon-separated list of attachment paths (optional)
   - status: Email status (pending/sent/failed)
   - email_sent_date: Date when email was sent

3. **Run the email campaign**
   ```bash
   python email_automation.py
   ```

## Email Template Customization

The HTML email template (`templates/email_template.html`) supports the following variables:
- ${first_name}: Recipient's first name
- ${last_name}: Recipient's last name
- ${custom_message}: Custom message for the recipient
- ${media_content}: Embedded images (automatically handled)
- ${sender_name}: Sender's name
- ${sender_title}: Sender's title
- ${company_name}: Company name

## Troubleshooting

1. **Check logs**
   - Look in the `logs` directory for detailed error messages
   - Each run creates a new log file with timestamp

2. **Common issues**
   - Azure permissions not granted
   - Invalid credentials in .env
   - Missing or incorrect file paths
   - Rate limiting (adjust in config.json)

## Security Notes

- Never commit `.env` file or any files containing credentials
- Regularly rotate your Azure application secrets
- Keep your `config.json` and `contacts.xlsx` private
- Use environment variables for all sensitive information

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 