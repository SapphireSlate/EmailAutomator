import pandas as pd

# Create sample data
data = {
    'email': ['your.email@example.com'],  # Replace with actual email
    'first_name': ['Your'],
    'last_name': ['Name'],
    'job_title': ['Your Title'],
    'company': ['Your Company'],
    'custom_message': [
        'Your custom message here.'
    ],
    'email_sent_date': [''],
    'status': ['pending']
}

# Create DataFrame with string dtypes
df = pd.DataFrame(data)

# Ensure status column is string type
df['status'] = df['status'].astype(str)

# Save to Excel with string types preserved
with pd.ExcelWriter('contacts.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, index=False)

print("contacts.xlsx file has been created successfully!")
print("\nCurrent contacts in file:")
print(df.to_string()) 