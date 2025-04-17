import os
import logging
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
from utils.sheets_helper import GoogleSheetsHelper
from utils.drive_helper import GoogleDriveHelper

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "gymlogclub-dev-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Add template context processor for current date/time
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Initialize Google API helpers with development mode until credentials are provided
sheets_helper = GoogleSheetsHelper()
drive_helper = GoogleDriveHelper()

# Global variables
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = '/tmp/gymlogclub_uploads'

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/set_user', methods=['POST'])
def set_user():
    """Set the current user in the session"""
    username = request.form.get('username')
    group_code = request.form.get('group_code')
    
    if not username:
        flash('Please provide a username', 'error')
        return redirect(url_for('index'))
    
    session['username'] = username
    session['group_code'] = group_code
    
    return redirect(url_for('feed'))

@app.route('/logout')
def logout():
    """Clear the user session"""
    session.pop('username', None)
    session.pop('group_code', None)
    return redirect(url_for('index'))

@app.route('/feed')
def feed():
    """Render the feed page with recent check-ins"""
    if 'username' not in session:
        return redirect(url_for('index'))
    
    # Get feed data from Google Sheets
    entries = sheets_helper.get_recent_entries(days=7)
    
    return render_template('feed.html', entries=entries, username=session['username'])

@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    """Handle gym check-in"""
    if 'username' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = session['username']
        workout_description = request.form.get('workout_description', '')
        
        image_url = None
        if 'workout_image' in request.files:
            file = request.files['workout_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                
                # Upload to Google Drive
                image_url = drive_helper.upload_file(file_path, filename)
                
                # Remove temporary file
                os.remove(file_path)
        
        # Log to Google Sheets
        sheets_helper.add_entry(username, workout_description, image_url)
        
        flash('Check-in successful!', 'success')
        return redirect(url_for('feed'))
    
    return render_template('checkin.html', username=session['username'])

@app.route('/api/group_members')
def get_group_members():
    """Get list of users who have checked in"""
    members = sheets_helper.get_unique_users()
    return jsonify(members)

@app.route('/api/feed_data')
def get_feed_data():
    """Get feed data for AJAX updates"""
    sort_by = request.args.get('sort_by', 'date')
    entries = sheets_helper.get_recent_entries(days=7, sort_by=sort_by)
    return jsonify(entries)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
