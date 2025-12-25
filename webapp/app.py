"""
News-Flash Web Application
Multi-user news aggregator with authentication and personalized topics.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from fetch_news import fetch_news
from summarize import summarize_news
from config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsflash.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'
app.config['REMEMBER_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_DOMAIN'] = None
app.config['SESSION_COOKIE_PATH'] = '/'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.session_protection = None

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    preferred_email_time = db.Column(db.String(5), default='08:00')  # Format: HH:MM
    email_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    preferences = db.relationship('NewsPreference', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class NewsPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    max_articles = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/whoami')
def whoami():
    return {
        'is_authenticated': bool(getattr(current_user, 'is_authenticated', False)),
        'id': getattr(current_user, 'id', None),
        'username': getattr(current_user, 'username', None)
    }

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        preferred_time = request.form.get('preferred_email_time', '08:00')
        email_enabled = request.form.get('email_enabled') == 'on'
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('signup'))
        
        user = User(username=username, email=email, preferred_email_time=preferred_time, email_enabled=email_enabled)
        user.set_password(password)
        db.session.add(user)
        
        # Add default topic
        default_pref = NewsPreference(user=user, topic='Technology', max_articles=10)
        db.session.add(default_pref)
        
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            print(f"[DEBUG] login: logged in user_id={user.id}, is_authenticated={current_user.is_authenticated}")
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Debug: check auth state
    print(f"[DEBUG] dashboard: is_authenticated={current_user.is_authenticated}, user_id={getattr(current_user, 'id', None)}")
    preferences = NewsPreference.query.filter_by(user_id=current_user.id).all()
    topic_choices = [
        "Technology",
        "Business",
        "Finance",
        "Markets",
        "Startups",
        "AI",
        "Cybersecurity",
        "Science",
        "Health",
        "Sports",
        "Entertainment",
        "Politics",
        "World",
        "India",
        "US",
        "Europe",
        "Climate",
        "Energy",
        "Space",
        "Education"
    ]
    return render_template('dashboard.html', preferences=preferences, topic_choices=topic_choices)

@app.route('/add_topic', methods=['POST'])
@login_required
def add_topic():
    topic = request.form.get('topic')
    max_articles = int(request.form.get('max_articles', 10))
    
    if topic:
        pref = NewsPreference(user_id=current_user.id, topic=topic, max_articles=max_articles)
        db.session.add(pref)
        db.session.commit()
        flash(f'Topic "{topic}" added successfully!', 'success')
    
    return redirect(url_for('dashboard'))

@app.route('/delete_topic/<int:topic_id>')
@login_required
def delete_topic(topic_id):
    pref = NewsPreference.query.get_or_404(topic_id)
    
    if pref.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(pref)
    db.session.commit()
    flash('Topic removed', 'info')
    return redirect(url_for('dashboard'))

@app.route('/news/<int:topic_id>')
@login_required
def view_news(topic_id):
    pref = NewsPreference.query.get_or_404(topic_id)
    
    if pref.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        # Fetch and summarize
        articles = fetch_news(topic=pref.topic, max_articles=pref.max_articles)
        
        if not articles:
            flash(f'No articles found for "{pref.topic}"', 'warning')
            return redirect(url_for('dashboard'))
        
        summary = summarize_news(articles)
        
        return render_template('news.html', 
                             topic=pref.topic, 
                             summary=summary, 
                             articles=articles)
    
    except Exception as e:
        flash(f'Error fetching news: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        preferred_time = request.form.get('preferred_email_time')
        email_enabled = request.form.get('email_enabled') == 'on'
        
        current_user.preferred_email_time = preferred_time
        current_user.email_enabled = email_enabled
        db.session.commit()
        
        flash('Email preferences updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
