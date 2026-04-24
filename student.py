import os
from flask import Blueprint, render_template, session, redirect, request
from models import Drive, Application, Student, db
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from config import Config

student_bp = Blueprint("student", __name__, url_prefix="/student")
ALLOWED_EXT = {"pdf", "doc", "docx"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


@student_bp.route("/dashboard")
def dashboard():
    if "student" not in session:
        return redirect("/")
    student = Student.query.get(session["student"])
    drives = Drive.query.filter_by(approved=True, closed=False).all()
    my_apps = Application.query.filter_by(student_id=session["student"]).all()
    applied_ids = {a.drive_id: a for a in my_apps}
    return render_template("student/dashboard.html",
        drives=drives, student=student,
        applied_ids=applied_ids, my_apps=my_apps)


@student_bp.route("/apply/<int:drive_id>")
def apply(drive_id):
    if "student" not in session:
        return redirect("/")
    student_id = session["student"]
    drive = Drive.query.get_or_404(drive_id)
    if not drive.approved or drive.closed:
        return redirect("/student/dashboard")
    existing = Application.query.filter_by(student_id=student_id, drive_id=drive_id).first()
    if not existing:
        application = Application(student_id=student_id, drive_id=drive_id)
        db.session.add(application)
        db.session.commit()
    return redirect("/student/dashboard")


@student_bp.route("/drive/<int:id>")
def drive_details(id):
    if "student" not in session:
        return redirect("/")
    drive = Drive.query.get_or_404(id)
    student_id = session["student"]
    already_applied = Application.query.filter_by(student_id=student_id, drive_id=id).first()
    return render_template("student/drive_details.html",
        drive=drive, already_applied=already_applied)


@student_bp.route("/history")
def history():
    if "student" not in session:
        return redirect("/")
    student = Student.query.get(session["student"])
    my_apps = Application.query.filter_by(student_id=session["student"]).order_by(Application.applied_at.desc()).all()
    return render_template("student/history.html", applications=my_apps, student=student)


@student_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if "student" not in session:
        return redirect("/")
    student = Student.query.get(session["student"])
    success = None
    error = None

    if request.method == "POST":
        student.name = request.form.get("name", student.name).strip()
        new_phone = request.form.get("phone", student.phone).strip()

        # Check phone uniqueness
        conflict = Student.query.filter(Student.phone == new_phone, Student.id != student.id).first()
        if conflict:
            error = "Phone number already in use."
        else:
            student.phone = new_phone
            cgpa = request.form.get("cgpa", "").strip()
            student.cgpa = float(cgpa) if cgpa else student.cgpa
            branch = request.form.get("branch", "").strip()
            student.branch = branch or student.branch
            grad = request.form.get("graduation_year", "").strip()
            student.graduation_year = int(grad) if grad else student.graduation_year

            new_pw = request.form.get("new_password", "").strip()
            if new_pw:
                student.password = generate_password_hash(new_pw)

            # Resume upload
            file = request.files.get("resume")
            if file and file.filename and allowed_file(file.filename):
                fname = secure_filename(f"resume_{student.id}_{file.filename}")
                os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(Config.UPLOAD_FOLDER, fname))
                student.resume_filename = fname

            db.session.commit()
            success = "Profile updated successfully!"

    return render_template("student/profile.html", student=student, success=success, error=error)
