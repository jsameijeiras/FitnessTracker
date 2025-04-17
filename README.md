# 🏋️‍♂️ GymLog Club

**Share your grind. Keep each other motivated.**

GymLog Club is a lightweight web application that allows a group of friends to log and view their gym activity through a clean and simple mobile-friendly interface. Users can check in daily, optionally upload training details and a photo, and see a daily/weekly report of everyone's activity.

## Features

- **Simple Identification**: Users identify themselves by entering a name or selecting from a dropdown of existing users. Optional group code for privacy.
- **Daily Check-In**: Track your gym attendance with a simple check-in process.
- **Optional Details**: Share what you trained and upload photos of your workout.
- **Group Feed**: View everyone's recent check-ins, sortable by date or person.
- **Mobile-Optimized UI**: Responsive design that works well on any device.

## Backend

The application uses Google Sheets as a backend database and Google Drive for image storage:

- Google Sheets stores check-in data (timestamp, username, workout description, image URL)
- Google Drive hosts uploaded workout photos
- Both are accessed through Google API clients in the Flask backend

## Setup

### Required Environment Variables

To use the Google Sheets and Drive APIs, the following environment variables are needed:

- `GOOGLE_SHEETS_API_KEY`: JSON credentials for Google Sheets API access
- `GOOGLE_DRIVE_API_KEY`: JSON credentials for Google Drive API access
- `GOOGLE_SHEET_ID`: ID of the Google Sheet to use for storing data
- `GOOGLE_DRIVE_FOLDER_ID`: ID of the Google Drive folder for storing images
- `SESSION_SECRET`: Secret key for Flask session encryption

Without these variables, the application runs in development mode with sample data.

### Running the Application

To start the server:

```
gunicorn --bind 0.0.0.0:5000 main:app
```

## Development

The application is built with:

- **Flask**: Python web framework
- **Bootstrap 5**: Responsive UI components
- **Google API Client**: For Sheets and Drive integration

## License

This project is licensed under the MIT License.