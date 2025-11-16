from datetime import datetime, timedelta
import json
import requests
from azure.identity import DeviceCodeCredential

# ---- CONFIG: EDIT THESE ----
TENANT_ID = "7f8d9146-b24b-431b-b08b-a5d78b0eb1b9"
TO_EMAIL = "techpi@3cw8wl.onmicrosoft.com"
CLIENT_ID = "804fd46c-707d-4ab1-8b71-c7144c0617e2"  # Replace with your Azure AD app registration client ID
# ----------------------------

def main():
    try:
        print("Starting authentication process...")
        
        # Initialize the Device Code credential
        credential = DeviceCodeCredential(
            tenant_id=TENANT_ID,
            client_id=CLIENT_ID
        )

        # Get access token with all required scopes
        scopes = [
            "https://graph.microsoft.com/User.Read",
            "https://graph.microsoft.com/Calendars.ReadWrite",
            "https://graph.microsoft.com/Mail.Send",
            "https://graph.microsoft.com/Files.ReadWrite",
            "https://graph.microsoft.com/Sites.Read.All"
        ]
        # Get token for each scope individually
        token = credential.get_token(scopes[0]).token
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print("Token obtained successfully")

        # Base URL for Microsoft Graph API
        base_url = "https://graph.microsoft.com/v1.0"

        # 1) Test basic profile access
        print("\n1. Testing profile access...")
        me_response = requests.get(f"{base_url}/me", headers=headers)
        me_response.raise_for_status()
        user_info = me_response.json()
        print(f"Successfully logged in as: {user_info.get('displayName')}")
        print(f"Email: {user_info.get('userPrincipalName')}")

        # 2) Create calendar event
        print("\n2. Creating calendar event...")
        start_time = datetime.utcnow() + timedelta(minutes=10)
        end_time = start_time + timedelta(minutes=30)

        event = {
            "subject": "Renewal activity event",
            "body": {
                "contentType": "Text",
                "content": "Auto-created to keep developer tenant active."
            },
            "start": {
                "dateTime": start_time.isoformat() + "Z",
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": end_time.isoformat() + "Z",
                "timeZone": "UTC"
            }
        }
        calendar_response = requests.post(
            f"{base_url}/me/events",
            headers=headers,
            json=event
        )
        calendar_response.raise_for_status()
        print("Calendar event created successfully")

        # 3) Send an email
        print("\n3. Sending email...")
        message = {
            "message": {
                "subject": "Developer Tenant Renewal Activity",
                "body": {
                    "contentType": "Text",
                    "content": "This message records recent tenant activity."
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": TO_EMAIL
                        }
                    }
                ]
            },
            "saveToSentItems": True
        }
        email_response = requests.post(
            f"{base_url}/me/sendMail",
            headers=headers,
            json=message
        )
        email_response.raise_for_status()
        print("Email sent successfully")

        # 4) Upload small file to OneDrive
        print("\n4. Uploading file to OneDrive...")
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
        filename = f"renewal-proof-{timestamp}.txt"
        content = f"Keep-alive at {datetime.utcnow().isoformat()}Z UTC"
        
        file_response = requests.put(
            f"{base_url}/me/drive/root:/{filename}:/content",
            headers={**headers, "Content-Type": "text/plain"},
            data=content.encode()
        )
        file_response.raise_for_status()
        print("File uploaded to OneDrive successfully")

        # 5) SharePoint sites (read)
        print("\n5. Accessing SharePoint sites...")
        sites_response = requests.get(f"{base_url}/sites?search=*", headers=headers)
        sites_response.raise_for_status()
        print("SharePoint sites accessed successfully")

        # 6) List upcoming calendar events
        print("\n6. Fetching upcoming calendar events...")
        events_response = requests.get(
            f"{base_url}/me/events?$select=subject,start,end&$orderby=start/dateTime&$top=5",
            headers=headers
        )
        events_response.raise_for_status()
        events = events_response.json().get('value', [])
        print("\nUpcoming calendar events:")
        for event in events:
            start = event['start']['dateTime']
            subject = event['subject']
            print(f"- {start}: {subject}")

        # 7) Search recent emails
        print("\n7. Searching recent emails...")
        emails_response = requests.get(
            f"{base_url}/me/messages?$select=subject,receivedDateTime&$orderby=receivedDateTime desc&$top=5",
            headers=headers
        )
        emails_response.raise_for_status()
        emails = emails_response.json().get('value', [])
        print("\nRecent emails:")
        for email in emails:
            received = email['receivedDateTime']
            subject = email['subject']
            print(f"- {received}: {subject}")

        # 8) List OneDrive files
        print("\n8. Listing OneDrive files...")
        files_response = requests.get(
            f"{base_url}/me/drive/root/children?$select=name,size,lastModifiedDateTime&$orderby=lastModifiedDateTime desc&$top=5",
            headers=headers
        )
        files_response.raise_for_status()
        files = files_response.json().get('value', [])
        print("\nRecent OneDrive files:")
        for file in files:
            name = file['name']
            modified = file['lastModifiedDateTime']
            size = file.get('size', 'N/A')
            print(f"- {modified}: {name} ({size} bytes)")

        # 9) Create a shared folder in OneDrive
        print("\n9. Creating a shared folder in OneDrive...")
        folder_name = f"Shared-Folder-{datetime.utcnow().strftime('%Y-%m-%d')}"
        folder_data = {
            "name": folder_name,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "rename"
        }
        folder_response = requests.post(
            f"{base_url}/me/drive/root/children",
            headers=headers,
            json=folder_data
        )
        folder_response.raise_for_status()
        folder_info = folder_response.json()
        print(f"Created folder: {folder_info['name']}")

        # 10) Share the folder
        share_data = {
            "type": "view",
            "scope": "organization"
        }
        share_response = requests.post(
            f"{base_url}/me/drive/items/{folder_info['id']}/createLink",
            headers=headers,
            json=share_data
        )
        share_response.raise_for_status()
        share_info = share_response.json()
        print(f"Folder shared. Link: {share_info['link']['webUrl']}")

        print("\n\033[92mAll operations completed successfully!\033[0m")
        print("\nSummary of new features:")
        print("- Listed 5 upcoming calendar events")
        print("- Showed 5 most recent emails")
        print("- Listed 5 most recent OneDrive files")
        print("- Created and shared a new folder in OneDrive")

        # 3) Send an email
        message = {
            "message": {
                "subject": "Developer Tenant Renewal Activity",
                "body": {
                    "contentType": "Text",
                    "content": "This message records recent tenant activity."
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": TO_EMAIL
                        }
                    }
                ]
            },
            "saveToSentItems": True
        }
        email_response = requests.post(
            f"{base_url}/me/sendMail",
            headers=headers,
            json=message
        )
        email_response.raise_for_status()
        print("Email sent")

        # 4) Upload small file to OneDrive
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
        filename = f"renewal-proof-{timestamp}.txt"
        content = f"Keep-alive at {datetime.utcnow().isoformat()}Z UTC"
        
        file_response = requests.put(
            f"{base_url}/me/drive/root:/{filename}:/content",
            headers={**headers, "Content-Type": "text/plain"},
            data=content.encode()
        )
        file_response.raise_for_status()
        print("File uploaded to OneDrive")

        # 5) SharePoint sites (read)
        sites_response = requests.get(f"{base_url}/sites?search=*", headers=headers)
        sites_response.raise_for_status()
        print("SharePoint sites accessed")

        print("\033[92mBurst activity completed across Mail, Calendar, OneDrive, SharePoint, and Graph.\033[0m")

    except Exception as e:
        print(f"\033[91mError: {str(e)}\033[0m")

if __name__ == "__main__":
    main()