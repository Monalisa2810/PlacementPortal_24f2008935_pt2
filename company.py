from flask import Blueprint, render_template, request, session, redirect
from models import db, Company, Drive, Application, Student

company_bp = Blueprint("company", __name__, url_prefix="/company")


def company_required():
    return "company" not in session


@company_bp.route("/dashboard")
def dashboard():
    if company_required():
        return redirect("/")
    company = Company.query.get(session["company"])
    drives = Drive.query.filter_by(company_id=session["company"]).all()
    drive_counts = {d.id: Application.query.filter_by(drive_id=d.id).count() for d in drives}
    return render_template("company/dashboard.html",
        company=company, drives=drives, drive_counts=drive_counts)


@company_bp.route("/create_drive", methods=["GET", "POST"])
def create_drive():
    if company_required():
        return redirect("/")
    company = Company.query.get(session["company"])
    if not company.approved:
        return render_template("company/dashboard.html", company=company,
            drives=[], drive_counts={},
            error="Your account is not yet approved by admin. You cannot create drives.")

    if request.method == "POST":
        drive = Drive(
            company_id=session["company"],
            job_title=request.form.get("job_title", "").strip(),
            description=request.form.get("description", "").strip(),
            eligibility=request.form.get("eligibility", "").strip(),
            deadline=request.form.get("deadline", "").strip(),
            package=request.form.get("package", "").strip(),
            location=request.form.get("location", "").strip(),
        )
        db.session.add(drive)
        db.session.commit()
        return redirect("/company/dashboard")

    return render_template("company/create_drive.html")


@company_bp.route("/edit_drive/<int:drive_id>", methods=["GET", "POST"])
def edit_drive(drive_id):
    if company_required():
        return redirect("/")
    drive = Drive.query.get_or_404(drive_id)
    if drive.company_id != session["company"]:
        return redirect("/company/dashboard")

    if request.method == "POST":
        drive.job_title = request.form.get("job_title", drive.job_title).strip()
        drive.description = request.form.get("description", drive.description).strip()
        drive.eligibility = request.form.get("eligibility", drive.eligibility).strip()
        drive.deadline = request.form.get("deadline", drive.deadline).strip()
        drive.package = request.form.get("package", drive.package or "").strip()
        drive.location = request.form.get("location", drive.location or "").strip()
        db.session.commit()
        return redirect("/company/dashboard")

    return render_template("company/edit_drive.html", drive=drive)


@company_bp.route("/close_drive/<int:drive_id>")
def close_drive(drive_id):
    if company_required():
        return redirect("/")
    drive = Drive.query.get_or_404(drive_id)
    if drive.company_id == session["company"]:
        drive.closed = True
        db.session.commit()
    return redirect("/company/dashboard")


@company_bp.route("/delete_drive/<int:drive_id>")
def delete_drive(drive_id):
    if company_required():
        return redirect("/")
    drive = Drive.query.get_or_404(drive_id)
    if drive.company_id == session["company"]:
        Application.query.filter_by(drive_id=drive_id).delete()
        db.session.delete(drive)
        db.session.commit()
    return redirect("/company/dashboard")


@company_bp.route("/applications/<int:drive_id>")
def applications(drive_id):
    if company_required():
        return redirect("/")
    drive = Drive.query.get_or_404(drive_id)
    if drive.company_id != session["company"]:
        return redirect("/company/dashboard")
    apps = Application.query.filter_by(drive_id=drive_id).all()
    items = [{"application": a, "student": Student.query.get(a.student_id)} for a in apps]
    return render_template("company/applications.html", items=items, drive=drive)


@company_bp.route("/update_status/<int:app_id>/<status>")
def update_status(app_id, status):
    if company_required():
        return redirect("/")
    if status not in ["Applied", "Shortlisted", "Selected", "Rejected"]:
        return redirect("/company/dashboard")
    app_obj = Application.query.get_or_404(app_id)
    drive = Drive.query.get(app_obj.drive_id)
    if drive and drive.company_id == session["company"]:
        app_obj.status = status
        db.session.commit()
    return redirect(f"/company/applications/{app_obj.drive_id}")


@company_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if company_required():
        return redirect("/")
    company = Company.query.get(session["company"])
    success = None
    if request.method == "POST":
        company.hr_contact = request.form.get("hr_contact", company.hr_contact).strip()
        company.website = request.form.get("website", company.website or "").strip()
        company.description = request.form.get("description", company.description or "").strip()
        db.session.commit()
        success = "Profile updated successfully!"
    return render_template("company/profile.html", company=company, success=success)
