from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, HospitalUser, DiseaseReport
from db_utils import add_disease_report, get_reports_grouped_by_location, get_recent_reports
import pandas as pd
import os
from collections import defaultdict

def create_app():
    app = Flask(__name__)
    
    # Secret key
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'cloudcure-secret-key'
    
    # Database: cloud if DATABASE_URL set, else local SQLite
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_monitor.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    # Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return HospitalUser.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app, login_manager

app, _ = create_app()

# === OUTBREAK DETECTION ===
def detect_outbreak(threshold=7):
    recent = get_recent_reports(days=7)
    if not recent:
        return {"status": "SAFE", "message": "No recent cases."}
    
    df = pd.DataFrame([{'location': r.location, 'disease': r.disease} for r in recent])
    location_counts = df['location'].value_counts()
    hotspots = location_counts[location_counts >= threshold].index.tolist()
    if hotspots:
        hotspot = hotspots[0]
        diseases = df[df['location'] == hotspot]['disease'].unique()
        disease_list = ", ".join([d.title() for d in diseases])
        return {
            "status": "ALERT",
            "message": f"⚠️ Possible outbreak in {hotspot} due to: {disease_list}",
            "hotspots": hotspots,
            "total_cases": int(location_counts[hotspot])
        }
    return {"status": "SAFE", "message": "No unusual activity detected."}


INDIA_LOCATION_COORDS = {
    "Ahmedabad-Ward5": (23.0225, 72.5714),
    "Ahmedabad-Ward7": (23.0300, 72.5800),
    "Mumbai-Dharavi": (19.0428, 72.8571),
    "Chennai-TNagar": (13.0415, 80.2340),
    "Kolkata-Howrah": (22.5958, 88.2820),
    "Delhi-East": (28.6304, 77.3530),
    "Bangalore-Central": (12.9716, 77.5946),
    "Hyderabad-Begumpet": (17.4474, 78.4746),
    "Pune-Kothrud": (18.5010, 73.7989),
    "Jaipur-MalviyaNagar": (26.8565, 75.8138),
}

# === ROUTES ===
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        hospital = request.form.get('hospital_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        if not (hospital and email and password):
            flash("All fields are required.", "error")
            return render_template('signup.html')
        if HospitalUser.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return render_template('signup.html')
        user = HospitalUser(hospital_name=hospital, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("✅ Account created! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = HospitalUser.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome, {user.hospital_name}!", "success")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('report_case'))
        else:
            flash("Invalid email or password.", "error")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

@app.route('/')
def home():
    # Fetch all reports (or recent ones)
    from db_utils import get_all_reports
    reports = get_all_reports()

    # Build map markers for known Indian locations
    map_markers = []
    for r in reports:
        coords = INDIA_LOCATION_COORDS.get(r.location)
        if coords:
            map_markers.append({
                "location": r.location,
                "disease": r.disease.title(),
                "patient_id": r.patient_id,
                "lat": coords[0],
                "lng": coords[1]
            })

    return render_template('index.html', alert=detect_outbreak(), map_markers=map_markers)

@app.route('/dashboard')
def dashboard():
    location_diseases = get_reports_grouped_by_location()
    all_reports = DiseaseReport.query.all()  # For showing decrypted notes
    return render_template('dashboard.html', location_diseases=location_diseases, all_reports=all_reports, alert=detect_outbreak())

# In app.py, inside /report route

@app.route('/report', methods=['GET', 'POST'])
@login_required
def report_case():
    if request.method == 'POST':
        pid = request.form.get('patient_id', '').strip()
        dis = request.form.get('disease', '').strip()
        loc = request.form.get('location', '').strip()
        days = request.form.get('days_ago', '0').strip()
        notes = request.form.get('notes', '').strip()  # New field

        if not (pid and dis and loc):
            flash("All fields are required!", "error")
            return render_template('report_form.html')

        try:
            add_disease_report(
                pid, 
                dis, 
                loc, 
                days, 
                notes if notes else None,  # Pass notes if exists
                current_user.id             # Pass hospital ID
            )
            flash(f"✅ Case of '{dis.title()}' reported in {loc}!", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"❌ Error saving report: {str(e)}", "error")
            return render_template('report_form.html')
    return render_template('report_form.html')

@app.route('/api/alert')
def api_alert():
    return jsonify(detect_outbreak())

if __name__ == '__main__':
    app.run(debug=True)