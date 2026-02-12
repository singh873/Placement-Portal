from .database import db
from datetime import datetime

# User Model (Admin and Student)

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    education = db.Column(db.String(50))
    cgpa = db.Column(db.String(50))
    address = db.Column(db.String(50))
    hobby = db.Column(db.String(50))


    # admin or student ka type & status
    type = db.Column(db.String(20), default="student", nullable=False)
    status = db.Column(db.String(20), default="active", nullable=False)

    applications = db.relationship("Application", backref="user")



# Company Model

class Company(db.Model):
    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    company_no = db.Column(db.Integer,nullable=False)
    website = db.Column(db.String(100),nullable=False)

    approval_status = db.Column(db.String(20), default="pending", nullable=False)
    status = db.Column(db.String(20), default="active", nullable=False)

    jobs = db.relationship("Jobs", backref="company")

# Placement Drive Model

class Jobs(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)

    job_title = db.Column(db.String(50), nullable=False)
    job_description = db.Column(db.String(200))
    eligibility = db.Column(db.String(100))
    salary = db.Column(db.Integer)
    location = db.Column(db.String(100))

    job_status = db.Column(db.String(20), default="pending", nullable=False)

    applications = db.relationship("Application", backref="jobs")


# Application Model

class Application(db.Model):
    __tablename__ = "application"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)

    status = db.Column(db.String(20), default="applied", nullable=False)
    applied_date = db.Column(db.DateTime, default=datetime.today)
