import pandas as pd
import os
from typing import List, Dict
import glob

def get_media_files(directory: str) -> List[str]:
    """Get all media files from a directory."""
    # Use a set to avoid duplicates
    files = set()
    print(f"\nSearching for media files in: {os.path.abspath(directory)}")
    
    for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        # Make case-insensitive by converting path to lowercase when checking
        found = glob.glob(os.path.join(directory, f'*{ext}')) + \
                glob.glob(os.path.join(directory, f'*{ext.upper()}'))
        if found:
            print(f"Found files with extension {ext}: {found}")
        files.update(found)
    
    # Convert to list and normalize paths
    normalized = sorted([os.path.normpath(f).replace('\\', '/') for f in files])
    print(f"\nMedia files found in {directory}:")
    for f in normalized:
        print(f"  - {f}")
        # Verify file exists
        if not os.path.exists(f):
            print(f"    WARNING: File does not exist: {f}")
    return normalized

def get_attachment_files(directory: str) -> List[str]:
    """Get all files from attachments directory."""
    print(f"\nSearching for attachments in: {os.path.abspath(directory)}")
    
    files = set(glob.glob(os.path.join(directory, '*.*')))
    normalized = sorted([os.path.normpath(f).replace('\\', '/') for f in files])
    print(f"\nAttachment files found in {directory}:")
    for f in normalized:
        print(f"  - {f}")
        # Verify file exists
        if not os.path.exists(f):
            print(f"    WARNING: File does not exist: {f}")
    return normalized

def reset_contacts():
    """Reset all contact statuses to pending and clear sent dates"""
    if os.path.exists('contacts.xlsx'):
        df = pd.read_excel('contacts.xlsx')
        df['status'] = 'pending'
        df['email_sent_date'] = ''
        with pd.ExcelWriter('contacts.xlsx', engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        print("All contact statuses have been reset to 'pending'")
    else:
        print("No existing contacts file found")

# Get available media and attachments
embeds = get_media_files('media/embeds')
attachments = get_attachment_files('media/attachments')

print("\nFound media files:", embeds)
print("Found attachment files:", attachments)

# Create sample data
data = {
    'email': [
        'sender@example.com',
        'recipient@example.com'
    ],
    'first_name': [
        'John',
        'Jane'
    ],
    'last_name': [
        'Doe',
        'Smith'
    ],
    'job_title': [
        'Manager',
        'Director'
    ],
    'company': [
        'Example Corp',
        'Demo Inc'
    ],
    'custom_message': [
        'This is a test email from our automated system.',
        'Check out our latest products and services!'
    ],
    'embedded_media': [
        '',  # First contact has no media
        ';'.join(embeds) if embeds else ''  # Second contact gets all media
    ],
    'attachments': [
        '',  # First contact has no attachments
        ';'.join(attachments) if attachments else ''  # Second contact gets all attachments
    ],
    'email_sent_date': ['', ''],
    'status': ['pending', 'pending']
}

if __name__ == "__main__":
    # Ask user what action to take
    action = input("Do you want to (1) create new contacts or (2) reset existing contacts? Enter 1 or 2: ")
    
    if action == "1":
        # Create new contacts file
        df = pd.DataFrame(data)
        df['status'] = df['status'].astype(str)
        
        # Print debug information
        print("\nMedia paths being added to contacts:")
        for i, path in enumerate(data['embedded_media']):
            print(f"Contact {i+1}: {path if path else 'None'}")
            if path:
                print(f"  File exists: {os.path.exists(path.split(';')[0] if ';' in path else path)}")
        
        print("\nAttachment paths being added to contacts:")
        for i, path in enumerate(data['attachments']):
            print(f"Contact {i+1}: {path if path else 'None'}")
            if path:
                print(f"  File exists: {os.path.exists(path.split(';')[0] if ';' in path else path)}")
        
        with pd.ExcelWriter('contacts.xlsx', engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        print("\nNew contacts.xlsx file has been created successfully!")
        
        # Print the full DataFrame for verification
        pd.set_option('display.max_colwidth', None)
        print("\nFull contacts data:")
        print(df.to_string())
    
    elif action == "2":
        # Reset existing contacts
        reset_contacts()
    
    else:
        print("Invalid option selected") 