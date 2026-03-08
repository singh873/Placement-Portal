# Placement Portal

## Project Description

The Placement Portal is a web application where students can apply for job opportunities and companies can post job openings. The platform connects students, companies, and administrators in a single system.

## Project Structure

```
Placement-Portal
│
├── application
│   ├── database.py
│   ├── models.py
│   └── controllers.py
│
├── static
│   ├── style.css
│   └── admin.css
│
├── templates
│   ├── login.html
│   ├── register.html
│   └── student_dash.html
│
├── app.py
├── README.md
```

## Tech Stack

```
Python
Flask
SQLite
HTML
CSS
SQLAlchemy
```

## Database Tables

```
Admin
Company
Student
JobPosition
Application
Placement
```

## Database Relationships

```
Company -> JobPosition (One to Many)
Student -> Application (One to Many)
JobPosition -> Application (One to Many)
Application -> Placement (One to One)
```

## How to Run the Project

```
git clone <repository_url>
cd Placement-Portal
pip install flask flask_sqlalchemy
python app.py
```

The SQLite database will be created automatically when the application runs.

## Milestone

```
Milestone-0 PPA-MAD-1
Milestone-PPA DB-Relationship
```
