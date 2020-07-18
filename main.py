from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)


@app.route("/")
def home():
    icon=url_for("static", filename="icon.svg")
    return render_template("index.html",icon=icon)

@app.route("/login/user", methods=["POST","GET"])
def user_login():
    if request.method == "POST":
        phone_number = request.form["phone_number"]
        user_email = request.form["user_email"]
        # This should be changed to add it to DB
        print(phone_number, user_email)
        return render_template(url_for("user_qr"))
    else:
        icon=url_for("static", filename="icon.svg")
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
    app.run(debug=True)
