import os
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from werkzeug.middleware.proxy_fix import ProxyFix
from models import db, User, Checkin
from sqlalchemy import extract, func, and_, desc

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "report-dev-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Add template context processor for current date/time
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/set_user', methods=['POST'])
def set_user():
    """Set the current user in the session"""
    username = request.form.get('username')
    group_name = request.form.get('group_code', 'Cabritinhas')
    
    if not username:
        flash('Por favor, ingresa tu nombre', 'error')
        return redirect(url_for('index'))
    
    # Check if user exists, if not create a new user
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, group_name=group_name)
            db.session.add(user)
            db.session.commit()
    
    session['username'] = username
    session['group_name'] = group_name
    
    return redirect(url_for('feed'))

@app.route('/logout')
def logout():
    """Clear the user session"""
    session.pop('username', None)
    session.pop('group_name', None)
    return redirect(url_for('index'))

@app.route('/feed')
def feed():
    """Render the feed page with recent check-ins"""
    if 'username' not in session:
        return redirect(url_for('index'))
    
    # Get recent checkins from database (last 7 days)
    seven_days_ago = datetime.now() - timedelta(days=7)
    checkins = Checkin.query.join(User).filter(
        Checkin.checkin_date >= seven_days_ago
    ).order_by(
        desc(Checkin.checkin_date)
    ).all()
    
    # Format data for template
    entries = []
    for checkin in checkins:
        entries.append({
            'id': checkin.id,
            'username': checkin.user.username,
            'workout_description': checkin.workout_description,
            'date': checkin.formatted_date,
            'time': checkin.formatted_time,
            'timestamp': checkin.checkin_date.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return render_template('feed.html', entries=entries, username=session['username'])

@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    """Handle gym check-in"""
    if 'username' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = session['username']
        workout_description = request.form.get('workout_description', '')
        
        # Find the user
        user = User.query.filter_by(username=username).first()
        if not user:
            # This should not happen as we create users in set_user
            flash('Usuario no encontrado', 'error')
            return redirect(url_for('index'))
        
        # Create a new checkin
        new_checkin = Checkin(
            user_id=user.id,
            workout_description=workout_description
        )
        db.session.add(new_checkin)
        db.session.commit()
        
        flash('¡Registro exitoso!', 'success')
        return redirect(url_for('feed'))
    
    return render_template('checkin.html', username=session['username'])

@app.route('/api/group_members')
def get_group_members():
    """Get list of users who have checked in"""
    users = User.query.all()
    usernames = [user.username for user in users]
    return jsonify(sorted(usernames))

@app.route('/api/feed_data')
def get_feed_data():
    """Get feed data for AJAX updates"""
    sort_by = request.args.get('sort_by', 'date')
    
    # Get recent checkins from database (last 7 days)
    seven_days_ago = datetime.now() - timedelta(days=7)
    query = Checkin.query.join(User).filter(Checkin.checkin_date >= seven_days_ago)
    
    if sort_by == 'person':
        query = query.order_by(User.username, desc(Checkin.checkin_date))
    else:
        query = query.order_by(desc(Checkin.checkin_date))
    
    checkins = query.all()
    
    # Format data for template
    entries = []
    for checkin in checkins:
        entries.append({
            'id': checkin.id,
            'username': checkin.user.username,
            'workout_description': checkin.workout_description,
            'date': checkin.formatted_date,
            'time': checkin.formatted_time,
            'timestamp': checkin.checkin_date.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify(entries)

@app.route('/leaderboard')
def leaderboard():
    """Show leaderboard of users with most checkins"""
    if 'username' not in session:
        return redirect(url_for('index'))
    
    try:
        # Get current week's start (Monday)
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        
        # Get current month's start
        start_of_month = datetime(today.year, today.month, 1).date()
        
        # Weekly leaderboard
        weekly_leaders = db.session.query(
            User.username,
            func.count(Checkin.id).label('checkin_count')
        ).join(Checkin, isouter=True).filter(
            func.date(Checkin.checkin_date) >= start_of_week
        ).group_by(
            User.username
        ).order_by(
            func.count(Checkin.id).desc()
        ).limit(10).all()
        
        # Monthly leaderboard
        monthly_leaders = db.session.query(
            User.username,
            func.count(Checkin.id).label('checkin_count')
        ).join(Checkin, isouter=True).filter(
            func.date(Checkin.checkin_date) >= start_of_month
        ).group_by(
            User.username
        ).order_by(
            func.count(Checkin.id).desc()
        ).limit(10).all()
        
        db.session.commit()
</old_str>
<new_str>
@app.route('/leaderboard')
def leaderboard():
    """Show leaderboard of users with most checkins"""
    if 'username' not in session:
        return redirect(url_for('index'))
    
    try:
        # Get current week's start (Monday)
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        
        # Get current month's start
        start_of_month = datetime(today.year, today.month, 1).date()
        
        # Weekly leaderboard
        weekly_leaders = db.session.query(
            User.username,
            func.count(Checkin.id).label('checkin_count')
        ).join(Checkin, isouter=True).filter(
            func.date(Checkin.checkin_date) >= start_of_week
        ).group_by(
            User.username
        ).order_by(
            func.count(Checkin.id).desc()
        ).limit(10).all()
        
        # Monthly leaderboard
        monthly_leaders = db.session.query(
            User.username,
            func.count(Checkin.id).label('checkin_count')
        ).join(Checkin, isouter=True).filter(
            func.date(Checkin.checkin_date) >= start_of_month
        ).group_by(
            User.username
        ).order_by(
            func.count(Checkin.id).desc()
        ).limit(10).all()
        
        return render_template(
            'leaderboard.html', 
            weekly_leaders=weekly_leaders,
            monthly_leaders=monthly_leaders,
            username=session['username']
        )
    except Exception as e:
        app.logger.error(f"Database error in leaderboard: {str(e)}")
        db.session.rollback()
        return render_template(
            'leaderboard.html',
            weekly_leaders=[],
            monthly_leaders=[],
            username=session['username']
        )
    
    return render_template(
        'leaderboard.html', 
        weekly_leaders=weekly_leaders,
        monthly_leaders=monthly_leaders,
        username=session['username']
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
