from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from qr_suite import encode_qr, decode_qr
import os

app = Flask(__name__)
app.secret_key = "Random word"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"

db = SQLAlchemy(app)

class users(db.Model):
    phone_number = db.Column("phone_number", db.Integer, primary_key=True)
    email = db.Column("email", db.String(100))

    def __init__(self, phone_number, email):
        self.phone_number = phone_number
        self.email = email

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
        icon=url_for("static", filename="icon.svg")
        return render_template("user_login.html",icon=icon)

@app.route("/user/qr")
def user_qr():
    icon=url_for("static", filename="icon.svg")
    path = session["img"]
    qr = f"../../static/user_qr/{path}"
    return render_template("user_qr.html",icon=icon, qr=qr)

@app.route("/user/scan")
def user_scan():
    icon=url_for("static", filename="icon.svg")
    camera=url_for("static", filename="temp_img.png")
    return render_template("user_scan.html",icon=icon, camera=camera)

@app.route("/login/operator", methods=["POST","GET"])
def operator_login():
    if request.method == "POST":
        operator_email = request.form["operator_email"]
        password = request.form["password"]
        # ADD TO DB
        print(operator_email, hash(password))
    else:
        icon=url_for("static", filename="icon.svg")
        return render_template("operator_login.html",icon=icon)

if __name__ == "__main__":
    os.system('rm ./static/user_qr/*')
    db.create_all()
    app.run(debug=True)
