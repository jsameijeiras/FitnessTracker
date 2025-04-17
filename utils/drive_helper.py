import os
import logging
import json
import random

# Handle import errors gracefully to allow development without Google APIs
try:
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
    from googleapiclient.http import MediaFileUpload
    GOOGLE_APIS_AVAILABLE = True
except ImportError:
    logging.warning("Google API libraries not available. Using development mode.")
    GOOGLE_APIS_AVAILABLE = False

class GoogleDriveHelper:
    def __init__(self):
        """Initialize the Google Drive API client"""
        self.service = None
        self.folder_id = None
        
        if not GOOGLE_APIS_AVAILABLE:
            logging.warning("Google Drive API not available. Operating in development mode.")
            return
            
        try:
            # Check if API key is in environment variable
            api_key_json = os.environ.get('GOOGLE_DRIVE_API_KEY')
            if api_key_json:
                credentials_info = json.loads(api_key_json)
                credentials = service_account.Credentials.from_service_account_info(
                    credentials_info,
                    scopes=['https://www.googleapis.com/auth/drive']
                )
                
                self.service = build('drive', 'v3', credentials=credentials)
                self.folder_id = os.environ.get('GOOGLE_DRIVE_FOLDER_ID', 'your-folder-id')
                logging.debug("Google Drive API initialized successfully from environment variable")
            elif os.path.exists('credentials.json'):
                # Use credentials file if it exists
                credentials = service_account.Credentials.from_service_account_file(
                    'credentials.json',
                    scopes=['https://www.googleapis.com/auth/drive']
                )
                
                self.service = build('drive', 'v3', credentials=credentials)
                self.folder_id = os.environ.get('GOOGLE_DRIVE_FOLDER_ID', 'your-folder-id')
                logging.debug("Google Drive API initialized successfully from credentials.json")
            else:
                logging.warning("No Google Drive credentials found. Operating in development mode.")
        except Exception as e:
            logging.error(f"Error initializing Google Drive API: {str(e)}")
            # Continue with minimal functionality for development
            
    def upload_file(self, file_path, file_name):
        """Upload a file to Google Drive and return the public URL"""
        if not self.service:
            logging.warning("Google Drive service not available, returning sample image URL")
            # Return a sample image URL for development mode
            sample_images = [
                'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600',
                'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600',
                'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600',
                'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=600',
                'https://images.unsplash.com/photo-1507398941214-572c25f4b1dc?w=600'
            ]
            import random
            return random.choice(sample_images)
            
        try:
            file_metadata = {
                'name': file_name,
                'parents': [self.folder_id]
            }
            
            media = MediaFileUpload(
                file_path,
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            file_id = file.get('id')
            
            # Set file to publicly accessible
            self.service.permissions().create(
                fileId=file_id,
                body={
                    'role': 'reader',
                    'type': 'anyone'
                }
            ).execute()
            
            # Get direct link to the file
            file_url = f"https://drive.google.com/uc?export=view&id={file_id}"
            
            logging.debug(f"File uploaded successfully: {file_url}")
            return file_url
        except Exception as e:
            logging.error(f"Error uploading file to Drive: {str(e)}")
            return None
