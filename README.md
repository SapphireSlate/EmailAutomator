# Email Automator

An automated email sending system built with Python and Microsoft Graph API. This application allows for automated email campaigns with customizable templates and contact management.

## Prerequisites

- Python 3.8 or higher
- Azure Account with registered application
- Microsoft 365 account with appropriate permissions

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd EmailAutomator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Azure Application**
   - Register a new application in Azure Portal
   - Add Microsoft Graph API permissions for Mail.Send
   - Grant admin consent for the required permissions
   - Note down the following values:
     - Client ID
     - Client Secret
     - Tenant ID

4. **Environment Setup**
   Create a `.env` file in the root directory with the following structure:
   ```
   CLIENT_ID=your_client_id
   CLIENT_SECRET=your_client_secret
   TENANT_ID=your_tenant_id
   USER_EMAIL=your_email@domain.com
   ```

## Usage

1. **Contact Management**
   - Update contacts in `create_contacts.py`
   - Run contact creation:
     ```bash
     python create_contacts.py
     ```

2. **Email Templates**
   - Customize email templates in `templates/email_template.html`
   - Update template variables in the code as needed

3. **Running the Application**
   ```bash
   python email_automation.py
   ```

## Features

- Automated email sending using Microsoft Graph API
- HTML email template support
- Contact management system
- Error handling and logging
- Campaign tracking

## Security Notes

- Never commit `.env` file or any sensitive credentials
- Use environment variables for all sensitive information
- Regularly rotate your Azure application secrets

## Troubleshooting

- Check Azure portal for correct permissions
- Verify all environment variables are set correctly
- Review logs for detailed error messages
- Ensure admin consent is granted for all required permissions

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[Your chosen license] 