from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from qr_suite import encode_qr, decode_qr
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "Random word"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_BINDS"] = {
    "users":"sqlite:///users.sqlite3",
    "operators":"sqlite:///operators.sqlite3"
}
app.config["UPLOAD_FOLDER"] = "./static/user_qr"

db = SQLAlchemy(app)

class users(db.Model):
    __bind_key__ = "users"
    phone_number = db.Column("phone_number", db.Integer, primary_key=True)
    email = db.Column("email", db.String(100))

    def __init__(self, phone_number, email):
        self.phone_number = phone_number
        self.email = email

class operators(db.Model):
    __bind_key__ = "operators"
    operator_email = db.Column("operator_email", db.String(100), primary_key=True)
    password = db.Column("password", db.String(100))

    def __init__(self, operator_email, password):
        self.operator_email = operator_email
        self.password = password

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
    qr=url_for("static", filename="temp_qr.png")
    if request.method == "POST":
        phone_number = request.form["phone_number"]
        user_email = request.form["user_email"]
        session.permanent = True

        found_user = users.query.filter_by(phone_number=phone_number).first()
        if found_user:
            print("User already exist")
        else:
            new_usr = users(phone_number, user_email)
            db.session.add(new_usr)
            db.session.commit()

        os.system(f"if test -e users/{phone_number}; then; rm users/{phone_number}; fi")
        session["img"] = encode_qr(phone_number)

        return redirect(url_for("user_qr"))
    else:
        return render_template("user_login.html",icon=icon)

@app.route("/user/qr", methods=["POST", "GET"])
def user_qr():
    if request.method == "POST":
            return redirect(url_for("user_scan"))
    else:
        icon=url_for("static", filename="icon.svg")
        path = session["img"]
        qr = f"../../static/user_qr/{path}"
        return render_template("user_qr.html",icon=icon, qr=qr)

@app.route("/user/scan", methods=["POST", "GET"])
def user_scan():
    if request.method == "POST":
        if request.form["opt"] == "generate":
            return redirect(url_for("user_qr"))
        else:
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
    icon=url_for("static", filename="icon.svg")
    camera=url_for("static", filename="temp_img.png")
    return render_template("user_scan.html",icon=icon, camera=camera)

@app.route("/new-user/qr")
def new_user_qr():
    icon=url_for("static", filename="icon.svg")
    qr=url_for("static", filename="temp_qr.png")
    return render_template("new_user_qr.html",icon=icon, qr=qr)

@app.route("/login/operator", methods=["POST","GET"])
def operator_login():
    if request.method == "POST":
        operator_email = request.form["operator_email"]
        password = request.form["password"]

        found_operator = operators.query.filter_by(operator_email=operator_email).first()

        if found_operator:
            if password == found_operator.password:
                return redirect(url_for("operator_qr"))
        else:
            return redirect(url_for("operator_relogin"))
    else:
        icon=url_for("static", filename="icon.svg")
        return render_template("operator_login.html",icon=icon)

@app.route("/operator/qr")
def operator_qr():
    icon=url_for("static", filename="icon.svg")
    qr=url_for("static", filename="temp_qr.png")
    return render_template("operator_qr.html",icon=icon, qr=qr)

@app.route("/operator/scan")
def operator_scan():
    icon=url_for("static", filename="icon.svg")
    camera=url_for("static", filename="temp_img.png")
    return render_template("operator_scan.html",icon=icon, camera=camera)

@app.route("/relogin/operator", methods=["POST", "GET"])
def operator_relogin():
    icon=url_for("static", filename="icon.svg")
    if request.method == "POST":
        operator_email = request.form["operator_email"]
        password = request.form["password"]

        found_operator = operators.query.filter_by(operator_email=operator_email).first()

        if found_operator:
            if password == found_operator.password:
                return redirect(url_for("operator_qr"))
        else:
            return redirect(url_for("operator_relogin"))
    return render_template("operator_relogin.html",icon=icon)

if __name__ == "__main__":
    os.system('rm ./static/user_qr/*')
    db.create_all()
    new_ope = operators("tot@gmail.com", "1234")
    db.session.add(new_ope)
    db.session.commit()
    app.run(debug=True)
