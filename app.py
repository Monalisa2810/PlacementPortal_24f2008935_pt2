import os
from flask import Flask
from config import Config
from models import db, Admin
from auth import auth_bp
from admin import admin_bp
from student import student_bp
from company import company_bp
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()
    from models import Admin
    from werkzeug.security import generate_password_hash
    if not Admin.query.filter_by(username="admin").first():
        admin = Admin(username="admin", password=generate_password_hash("admin123"))
        db.session.add(admin)
        db.session.commit()

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)
app.register_blueprint(company_bp)

if __name__ == "__main__":
    os.makedirs(os.path.join(os.path.dirname(__file__), "database"), exist_ok=True)
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    with app.app_context():
        db.create_all()
        if not Admin.query.filter_by(username="admin").first():
            admin = Admin(username="admin", password=generate_password_hash("admin123"))
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin created → username: admin | password: admin123")
    app.run(debug=True)
