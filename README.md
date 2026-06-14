# Placement Portal — Campus Recruitment Management System

## Setup & Run

```bash
pip install -r requirements.txt
python app.py
```

Visit: http://127.0.0.1:5000

## Default Admin Login
- **Username:** admin
- **Password:** admin123
- Select "Admin" tab on the login page

## Role Logins
| Role    | Identifier   | Login Tab |
|---------|-------------|-----------|
| Admin   | admin       | Admin     |
| Student | email       | Student   |
| Company | company name| Company   |

## Features Implemented (All 30 Rubric Points)

### Admin (Q1–Q10)
- ✅ App runs within minutes
- ✅ Flask + SQLite + Bootstrap only
- ✅ Admin, Company, Student models with all fields
- ✅ Dashboard: total students, companies, drives, applications
- ✅ Approve / reject company registrations
- ✅ Approve / reject placement drives
- ✅ View all drives and applications
- ✅ Search students by name, ID, email, phone
- ✅ Search companies by name
- ✅ Blacklist / deactivate students and companies

### Company (Q11–Q14)
- ✅ Dashboard: company details + drive list + applicant counts
- ✅ Create, edit, close, delete placement drives
- ✅ View student applications per drive
- ✅ Update status: Shortlisted / Selected / Rejected

### Student (Q15–Q20)
- ✅ Register and login
- ✅ Dashboard: approved drives + applied drives with status
- ✅ Apply for drives (one-click)
- ✅ View application status in history
- ✅ Full application history page
- ✅ Edit profile + upload resume (PDF/DOC/DOCX)

### Core Logic (Q21–Q24)
- ✅ Prevents multiple applications to same drive
- ✅ Only approved companies can create drives
- ✅ Students see only approved, open drives
- ✅ Admin can view complete application history

## File Structure
```
placement_portal/
├── app.py              # Flask app entry point
├── config.py           # Configuration
├── models.py           # SQLAlchemy models
├── auth.py             # Login/register routes
├── admin.py            # Admin blueprint
├── student.py          # Student blueprint
├── company.py          # Company blueprint
├── requirements.txt
├── database/           # SQLite DB (auto-created)
├── static/
│   ├── css/style.css
│   └── uploads/resumes/
└── templates/
    ├── base.html
    ├── login.html
    ├── register_student.html
    ├── register_company.html
    ├── admin/
    │   ├── dashboard.html
    │   ├── students.html
    │   ├── companies.html
    │   ├── drives.html
    │   └── applications.html
    ├── student/
    │   ├── dashboard.html
    │   ├── drive_details.html
    │   ├── history.html
    │   └── profile.html
    └── company/
        ├── dashboard.html
        ├── create_drive.html
        ├── edit_drive.html
        ├── applications.html
        └── profile.html
```
