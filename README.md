# 🧑‍💼 Job Board Web Application

This is a full-featured Job Board web application built with **Flask**. It supports multiple user roles (employer & seeker), job posting, application tracking, resume uploads, and an admin dashboard to manage users and jobs.

---

## 🚀 Features

- 👥 **User Roles**: Employer and Job Seeker
- 🔐 **Authentication**: Register/Login with role-based dashboards
- 📄 **Employers**:
  - Post new job openings
  - Edit/delete posted jobs
  - View applicants
- 📄 **Job Seekers**:
  - Upload resume
  - Search and apply for jobs
- 🛠️ **Admin Dashboard** (Custom-built):
  - View all users
  - View all jobs
  - View job applications
- 📦 **PostgreSQL** as the backend database
- 🌐 Hosted on [Render](https://render.com)
- 🎨 Responsive UI with Bootstrap

---

## 📸 Screenshots

> Replace the image filenames with your actual screenshot files

### Employer Dashboard
![Employer Dashboard](app/static/screenshots/employer_dashboard.png)

### Job Seeker Dashboard
![Seeker Dashboard](app/static/screenshots/seeker_dashboard.png)


## 🛠️ Technologies Used

- Python 3.11+
- Flask
- Flask-Login, Flask-WTF, Flask-Mail
- SQLAlchemy + PostgreSQL
- Jinja2 Templating
- Bootstrap 5
- Gunicorn (for deployment)

---

## 📁 Folder Structure

jobboard-app/
│
├── app/
│ ├── init.py
│ ├── models.py
│ ├── routes.py
│ └── ...
│
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── dashboard.html
│ └── ...
│
├── static/
│ ├── style.css
│ ├── images/
│ └── uploads/
│
├── .env
├── requirements.txt
├── render.yaml
├── wsgi.py
├── Procfile
└── README.md


---

## 🧪 Local Setup

1. **Clone the repo**  
   ```bash
   git clone https://github.com/Ifrah-c/jobboard-app.git
   cd jobboard-app


2. Create a virtual environment

bash

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate


3. Install dependencies

bash

pip install -r requirements.txt


4. Configure environment

Create a .env file and add the following:

env

SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=postgresql://user:password@host:port/dbname
MAIL_SERVER=
MAIL_PORT=
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_password



5. Run the app

bash

flask db init
flask db migrate
flask db upgrade
flask run



🌍 Deploy on Render

1. Create render.yaml

yaml

services:
  - type: web
    name: jobboard-app
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn wsgi:app"
    envVars:
      - key: FLASK_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: jobboard-db
          property: connectionString



2. Push code to GitHub

bash

git add .
git commit -m "Initial commit"
git push origin main


3. Connect GitHub to Render and deploy.

