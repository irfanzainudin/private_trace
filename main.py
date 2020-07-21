from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from qr_suite import encode_qr, decode_qr
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from config import SECRET_KEY, USER_DB, USER_QR, OPER_DB, OPER_QR
import os

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = USER_DB
app.config["SQLALCHEMY_BINDS"] = {
    "users":USER_DB,
    "operators":OPER_DB
}
app.config["UPLOAD_FOLDER"] = USER_QR

db = SQLAlchemy(app)

class users(UserMixin, db.Model):
    __bind_key__ = "users"
    phone_number = db.Column("phone_number", db.Integer, primary_key=True)
    email = db.Column("email", db.String(100))

    def __init__(self, phone_number, email):
        self.phone_number = phone_number
        self.email = email

class operators(UserMixin, db.Model):
    __bind_key__ = "operators"
    id = db.Column(db.Integer, primary_key=True)
    operator_email = db.Column("operator_email", db.String(100), unique=True)
    password = db.Column("password", db.String(100))

    def __init__(self, operator_email, password):
        self.operator_email = operator_email
        self.password = password

login_manager = LoginManager()
login_manager.login_view = "operator_login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(ope_id):
    return operators.query.get(int(ope_id))

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if request.form["account_type"] == "user":
            return redirect(url_for("user_login"))
        else:
            return redirect(url_for("operator_login"))
    else:
        icon=url_for("static", filename="icon.svg")
        return render_template("index.html",icon=icon)

@app.route("/login/user", methods=["POST","GET"])
def user_login():
    icon=url_for("static", filename="icon.svg")
    if request.method == "POST":
        phone_number = request.form["phone_number"]
        user_email = request.form["user_email"]
        session.permanent = True

        found_user = users.query.filter_by(phone_number=phone_number).first()
        if found_user:
            print("User already exist")
        else:
            flash("Welcome! You are automatically signed up to get you to use the app quicky.")
            new_usr = users(generate_password_hash(phone_number, method='sha256'), user_email)
            db.session.add(new_usr)
            db.session.commit()

        os.system(f"if test -e users/{phone_number}; then; rm users/{phone_number}; fi")
        session["img"] = encode_qr(phone_number)

        return redirect(url_for("user_qr"))
    else:
        return render_template("user_login.html",icon=icon)

@app.route("/user/qr")
def user_qr():
    icon=url_for("static", filename="icon.svg")
    path = session["img"]
    qr = f"../../static/user_qr/{path}"
    return render_template("user_qr.html",icon=icon, qr=qr)

@app.route("/user/scan", methods=["POST", "GET"])
def user_scan():
    icon=url_for("static", filename="icon.svg")
    if request.method == "POST":
        f = request.files["file"]
        file_name = secure_filename(f.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
        f.save(path)
        uid_restaurant = decode_qr(path)
        if not uid_restaurant:
            flash("No QR detected, scan again")
        else:
            return render_template("user.html", uid_restaurant=uid_restaurant)

    flash("Nothing scanned yet")
    return render_template("user_scan.html",icon=icon)

@app.route("/signup/operator", methods=["POST", "GET"])
def operator_signup():
    icon=url_for("static", filename="icon.svg")
    if request.method == "POST":
        operator_email = request.form["operator_email"]
        password = request.form["password"]

        operator = operators.query.filter_by(operator_email=operator_email).first()

        # TODO
        if operator:
            flash("Email already exists")
            return redirect(url_for("operator_signup"))
        else:
            new_ope = operators(operator_email, generate_password_hash(password, method='sha256'))
            db.session.add(new_ope)
            db.session.commit()

            return redirect(url_for("operator_login"))
    else:
        return render_template("operator_signup.html",icon=icon)

@app.route("/login/operator", methods=["POST","GET"])
def operator_login():
    icon=url_for("static", filename="icon.svg")
    if request.method == "POST":
        operator_email = request.form["operator_email"]
        password = request.form["password"]
        # session.permanent = True

        operator = operators.query.filter_by(operator_email=operator_email).first()

        if not operator or not check_password_hash(operator.password, password):
            flash("Please check your login credentials and try again.")
            return redirect(url_for("operator_login"))
        else:
            session["img"] = encode_qr(operator_email)
            login_user(operator, remember=False)
            return redirect(url_for("operator_qr"))
    else:
        return render_template("operator_login.html",icon=icon)

@app.route("/operator/qr", methods=["POST", "GET"])
@login_required
def operator_qr():
    if request.method == "POST":
        if request.form["action_btn"] == "logout":
            logout_user()
            return redirect(url_for("operator_login"))
    icon=url_for("static", filename="icon.svg")
    path = session["img"]
    qr = f"../../static/user_qr/{path}"
    return render_template("operator_qr.html", icon=icon, qr=qr, email=current_user.operator_email)

@app.route("/operator/scan", methods=["POST", "GET"])
@login_required
def operator_scan():
    icon=url_for("static", filename="icon.svg")
    if request.method == "POST":
        if request.form["action_btn"] == "logout":
            logout_user()
            return redirect(url_for("operator_login"))
        f = request.files["file"]
        file_name = secure_filename(f.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
        f.save(path)
        uid_restaurant = decode_qr(path)
        if not uid_restaurant:
            flash("No QR detected, scan again")
        else:
            return render_template("operator.html", uid_restaurant=uid_restaurant)

    flash("Nothing scanned yet")
    return render_template("operator_scan.html", icon=icon, email=current_user.operator_email)

@app.route("/logout/user", methods=["POST", "GET"])
def user_logout():
    return render_template("user_logout.html")

@app.route("/logout/operator", methods=["POST", "GET"])
@login_required
def operator_logout():
    logout_user()
    return render_template("operator_logout.html")

if __name__ == "__main__":
    os.system('rm ./static/user_qr/*')
    db.create_all()
    app.run(debug=True)
