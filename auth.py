from flask import Blueprint, render_template, request, redirect, session
from models import db, Student, Company, Admin
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "student")

        if role == "admin":
            admin = Admin.query.filter_by(username=identifier).first()
            if admin and check_password_hash(admin.password, password):
                session["admin"] = admin.id
                return redirect("/admin/dashboard")
            return render_template("login.html", error="Invalid admin credentials.")

        elif role == "student":
            student = Student.query.filter_by(email=identifier).first()
            if student and check_password_hash(student.password, password):
                if student.blacklisted:
                    return render_template("login.html", error="Your account has been blacklisted. Contact the placement cell.")
                session["student"] = student.id
                return redirect("/student/dashboard")
            return render_template("login.html", error="Invalid email or password.")

        elif role == "company":
            company = Company.query.filter_by(name=identifier).first()
            if company and check_password_hash(company.password, password):
                if company.blacklisted:
                    return render_template("login.html", error="Your company account has been blacklisted.")
                if not company.approved:
                    return render_template("login.html", error="Your company is pending admin approval. Please wait.")
                session["company"] = company.id
                return redirect("/company/dashboard")
            return render_template("login.html", error="Invalid company name or password.")

    return render_template("login.html")


@auth_bp.route("/register_student", methods=["GET", "POST"])
def register_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        branch = request.form.get("branch", "").strip()
        cgpa = request.form.get("cgpa", "").strip()
        graduation_year = request.form.get("graduation_year", "").strip()

        if Student.query.filter_by(email=email).first():
            return render_template("register_student.html", error="Email already registered. Please login.")
        if Student.query.filter_by(phone=phone).first():
            return render_template("register_student.html", error="Phone number already registered.")

        student = Student(
            name=name,
            email=email,
            phone=phone,
            password=generate_password_hash(password),
            branch=branch or None,
            cgpa=float(cgpa) if cgpa else None,
            graduation_year=int(graduation_year) if graduation_year else None,
        )
        db.session.add(student)
        db.session.commit()
        return redirect("/")

    return render_template("register_student.html")


@auth_bp.route("/register_company", methods=["GET", "POST"])
def register_company():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        hr_contact = request.form.get("hr_contact", "").strip()
        website = request.form.get("website", "").strip()
        description = request.form.get("description", "").strip()
        password = request.form.get("password", "")

        if Company.query.filter_by(name=name).first():
            return render_template("register_company.html", error="Company name already registered.")

        company = Company(
            name=name,
            hr_contact=hr_contact,
            website=website,
            description=description,
            password=generate_password_hash(password),
        )
        db.session.add(company)
        db.session.commit()
        return render_template("register_company.html", success="Registration submitted! Await admin approval before logging in.")

    return render_template("register_company.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
