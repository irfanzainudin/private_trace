from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route("/")
def home():
    icon=url_for("static", filename="icon.svg")
    return render_template("index.html",icon=icon)

@app.route("/login/user")
def user_login():
    icon=url_for("static", filename="icon.svg")
    return render_template("user_login.html",icon=icon)

@app.route("/login/operator")
def operator_login():
    icon=url_for("static", filename="icon.svg")
    return render_template("operator_login.html",icon=icon)

@app.route("/user/email")
def get_email():
    icon=url_for("static", filename="icon.svg")
    return render_template("get_email.html",icon=icon)

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


if __name__ == "__main__":
    app.run(debug=True)
