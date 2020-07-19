from flask import Flask, render_template, url_for, request, redirect
# from firebase_admin import credentials, firestore, initialize_app
app = Flask(__name__)

# initialize firestore db
# cred = credentials.Certificate('key.json')
# default_app = initialize_app(cred)
# db = firestore.client()
# users_ref = db.collection('users')

def authenticate_user(phone_number):
    f = open("users.txt", "r")
    for line in f:
        if line == phone_number + '\n':
            f.close()
            return True
    f.close()
    return False

def add_user(phone_number):
    f = open("users.txt", "a")
    f.write(phone_number + '\n')
    f.close()

def authenticate_operator(operator_email, password):
    f = open("operators.txt", "r")
    for line in f:
        if line == operator_email + '+' + password + '\n':
            f.close()
            return True
    f.close()
    return False

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
        # This should be changed to add it to DB
        if authenticate_user(phone_number):
            return redirect(url_for("user_qr"))
        else:
            add_user(phone_number)
            return redirect(url_for("new_user_qr"))
    else:
        return render_template("user_login.html",icon=icon)

@app.route("/user/qr")
def user_qr():
    icon=url_for("static", filename="icon.svg")
    qr=url_for("static", filename="temp_qr.png")
    return render_template("user_qr.html",icon=icon, qr=qr)

@app.route("/user/scan")
def user_scan():
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
        # ADD TO DB
        if authenticate_operator(operator_email, password):
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
        # ADD TO DB
        if authenticate_operator(operator_email, password):
            return redirect(url_for("operator_qr"))
        else:
            return redirect(url_for("operator_relogin"))
    return render_template("operator_relogin.html",icon=icon)

if __name__ == "__main__":
    app.run(debug=True)
