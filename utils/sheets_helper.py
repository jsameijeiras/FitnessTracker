import os
import logging
from datetime import datetime, timedelta
import json

# Handle import errors gracefully to allow development without Google APIs
try:
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
    GOOGLE_APIS_AVAILABLE = True
except ImportError:
    logging.warning("Google API libraries not available. Using development mode.")
    GOOGLE_APIS_AVAILABLE = False

class GoogleSheetsHelper:
    def __init__(self):
        """Initialize the Google Sheets API client"""
        self.service = None
        self.spreadsheet_id = None
        self.sheet_name = 'GymLog'
        
        if not GOOGLE_APIS_AVAILABLE:
            logging.warning("Google Sheets API not available. Operating in development mode.")
            return
            
        try:
            # Check if API key is in environment variable
            api_key_json = os.environ.get('GOOGLE_SHEETS_API_KEY')
            if api_key_json:
                credentials_info = json.loads(api_key_json)
                credentials = service_account.Credentials.from_service_account_info(
                    credentials_info,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
                
                self.service = build('sheets', 'v4', credentials=credentials)
                self.spreadsheet_id = os.environ.get('GOOGLE_SHEET_ID', 'your-spreadsheet-id')
                logging.debug("Google Sheets API initialized successfully from environment variable")
            elif os.path.exists('credentials.json'):
                # Use credentials file if it exists
                credentials = service_account.Credentials.from_service_account_file(
                    'credentials.json',
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
                
                self.service = build('sheets', 'v4', credentials=credentials)
                self.spreadsheet_id = os.environ.get('GOOGLE_SHEET_ID', 'your-spreadsheet-id')
                logging.debug("Google Sheets API initialized successfully from credentials.json")
            else:
                logging.warning("No Google Sheets credentials found. Operating in development mode.")
        except Exception as e:
            logging.error(f"Error initializing Google Sheets API: {str(e)}")
            # Continue with minimal functionality for development
        
    def add_entry(self, username, workout_description='', image_url=None):
        """Add a new check-in entry to the Google Sheet"""
        if not self.service:
            logging.warning("Google Sheets service not available, skipping add_entry")
            return False
            
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            row_data = [
                timestamp,
                username,
                workout_description,
                image_url if image_url else ''
            ]
            
            body = {
                'values': [row_data]
            }
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f'{self.sheet_name}!A:D',
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            logging.debug(f"Sheet update result: {result}")
            return True
        except Exception as e:
            logging.error(f"Error adding entry to sheet: {str(e)}")
            return False
    
    def get_recent_entries(self, days=7, sort_by='date'):
        """Get recent entries from the Google Sheet"""
        if not self.service:
            logging.warning("Google Sheets service not available, returning sample data")
            # Return sample data for development
            sample_entries = [
                {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'username': 'Alice',
                    'workout_description': 'Leg day! 3x10 squats, 3x10 lunges, 2x15 leg presses',
                    'image_url': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600',
                    'date': datetime.now().strftime('%Y-%m-%d')
                },
                {
                    'timestamp': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
                    'username': 'Bob',
                    'workout_description': 'Morning run, 5km in 25 minutes',
                    'image_url': 'https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=600',
                    'date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                },
                {
                    'timestamp': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
                    'username': 'Charlie',
                    'workout_description': 'Upper body: bench press, shoulder press, pull-ups',
                    'image_url': 'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600',
                    'date': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
                }
            ]
            
            # Sort sample entries based on sort_by parameter
            if sort_by == 'person':
                sample_entries.sort(key=lambda x: x['username'])
            
            return sample_entries
            
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f'{self.sheet_name}!A:D'
            ).execute()
            
            rows = result.get('values', [])
            
            if not rows:
                return []
                
            headers = rows[0]
            entries = []
            
            # Calculate cutoff date
            cutoff_date = datetime.now() - timedelta(days=days)
            
            for row in rows[1:]:  # Skip header row
                # Ensure row has all columns
                while len(row) < 4:
                    row.append('')
                    
                timestamp, username, workout, image_url = row
                
                try:
                    entry_date = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                    if entry_date >= cutoff_date:
                        entries.append({
                            'timestamp': timestamp,
                            'username': username,
                            'workout_description': workout,
                            'image_url': image_url,
                            'date': entry_date.strftime('%Y-%m-%d')
                        })
                except ValueError:
                    # Skip entries with invalid date format
                    continue
            
            # Sort entries based on sort_by parameter
            if sort_by == 'person':
                entries.sort(key=lambda x: (x['username'], x['timestamp']), reverse=True)
            else:  # Default: sort by date
                entries.sort(key=lambda x: x['timestamp'], reverse=True)
                
            return entries
        except Exception as e:
            logging.error(f"Error getting entries from sheet: {str(e)}")
            return []
    
    def get_unique_users(self):
        """Get a list of unique users who have checked in"""
        if not self.service:
            logging.warning("Google Sheets service not available, returning sample data")
            # Return sample usernames for development
            return ['Alice', 'Bob', 'Charlie', 'David', 'Emma']
            
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f'{self.sheet_name}!B:B'
            ).execute()
            
            rows = result.get('values', [])
            
            if not rows:
                return []
                
            # Skip header row, get unique usernames
            usernames = set()
            for row in rows[1:]:
                if row and row[0].strip():
                    usernames.add(row[0])
                    
            return sorted(list(usernames))
        except Exception as e:
            logging.error(f"Error getting unique users: {str(e)}")
            return []
