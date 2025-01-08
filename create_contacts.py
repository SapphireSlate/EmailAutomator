import pandas as pd

# Create sample data
data = {
    'email': ['rciii95@gmail.com'],
    'first_name': ['RC'],
    'last_name': ['Test'],
    'company_name': ['Sweet Places'],
    'custom_message': [
        'This is a test email from The Sweet Places automated system.'
    ],
    'sender_name': ['The Sweet Places Team'],
    'sender_title': ['Customer Service']
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel file with the proper engine
df.to_excel('contacts.xlsx', index=False, engine='openpyxl')

print("contacts.xlsx file has been created successfully!") 