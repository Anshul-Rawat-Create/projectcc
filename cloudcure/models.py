from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class HospitalUser(UserMixin, db.Model):
    __tablename__ = 'hospital_users'
    id = db.Column(db.Integer, primary_key=True)
    hospital_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class DiseaseReport(db.Model):
    __tablename__ = 'disease_reports'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(50), nullable=False)
    disease = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    days_ago = db.Column(db.Integer, nullable=False)