from flask import Blueprint, render_template, redirect, session, request
from models import db, Student, Company, Drive, Application

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required():
    return "admin" not in session


@admin_bp.route("/dashboard")
def dashboard():
    if admin_required():
        return redirect("/")
    students = Student.query.all()
    companies = Company.query.all()
    drives = Drive.query.all()
    applications = Application.query.all()
    return render_template("admin/dashboard.html",
        students=students, companies=companies,
        drives=drives, applications=applications)


@admin_bp.route("/students")
def students():
    if admin_required():
        return redirect("/")
    q = request.args.get("q", "").strip()
    if q:
        results = Student.query.filter(
            db.or_(
                Student.name.ilike(f"%{q}%"),
                Student.email.ilike(f"%{q}%"),
                Student.phone.ilike(f"%{q}%"),
            )
        ).all()
        if q.isdigit():
            by_id = Student.query.filter_by(id=int(q)).first()
            if by_id and by_id not in results:
                results.append(by_id)
    else:
        results = Student.query.all()
    return render_template("admin/students.html", students=results, q=q)


@admin_bp.route("/companies")
def companies():
    if admin_required():
        return redirect("/")
    q = request.args.get("q", "").strip()
    if q:
        results = Company.query.filter(Company.name.ilike(f"%{q}%")).all()
    else:
        results = Company.query.all()
    return render_template("admin/companies.html", companies=results, q=q)


@admin_bp.route("/drives")
def drives():
    if admin_required():
        return redirect("/")
    drives = Drive.query.all()
    return render_template("admin/drives.html", drives=drives)


@admin_bp.route("/applications")
def applications():
    if admin_required():
        return redirect("/")
    apps = Application.query.order_by(Application.applied_at.desc()).all()
    return render_template("admin/applications.html", applications=apps)


@admin_bp.route("/approve_company/<int:id>")
def approve_company(id):
    if admin_required():
        return redirect("/")
    company = Company.query.get_or_404(id)
    company.approved = True
    db.session.commit()
    return redirect("/admin/companies")


@admin_bp.route("/reject_company/<int:id>")
def reject_company(id):
    if admin_required():
        return redirect("/")
    company = Company.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    return redirect("/admin/companies")


@admin_bp.route("/blacklist_company/<int:id>")
def blacklist_company(id):
    if admin_required():
        return redirect("/")
    company = Company.query.get_or_404(id)
    company.blacklisted = not company.blacklisted
    db.session.commit()
    return redirect("/admin/companies")


@admin_bp.route("/approve_drive/<int:id>")
def approve_drive(id):
    if admin_required():
        return redirect("/")
    drive = Drive.query.get_or_404(id)
    drive.approved = True
    db.session.commit()
    return redirect("/admin/drives")


@admin_bp.route("/reject_drive/<int:id>")
def reject_drive(id):
    if admin_required():
        return redirect("/")
    drive = Drive.query.get_or_404(id)
    db.session.delete(drive)
    db.session.commit()
    return redirect("/admin/drives")


@admin_bp.route("/blacklist_student/<int:id>")
def blacklist_student(id):
    if admin_required():
        return redirect("/")
    student = Student.query.get_or_404(id)
    student.blacklisted = not student.blacklisted
    db.session.commit()
    return redirect("/admin/students")


@admin_bp.route("/delete_student/<int:id>")
def delete_student(id):
    if admin_required():
        return redirect("/")
    student = Student.query.get_or_404(id)
    Application.query.filter_by(student_id=id).delete()
    db.session.delete(student)
    db.session.commit()
    return redirect("/admin/students")
