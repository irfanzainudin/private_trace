from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)


@app.route("/")
def home():
    icon=url_for("static", filename="icon.svg")
    return render_template("index.html",icon=icon)

@app.route("/login/user", methods=["POST","GET"])
def user_login():
    if request.method == "POST":
        if request.form["option-btn"] == "yes":
            phone_number = request.form["phone_number"]
            print(phone_number)
            return redirect(url_for("user_qr"))
        else:
            return redirect(url_for("get_email"))
    else:
        icon=url_for("static", filename="icon.svg")
        return render_template("user_login.html",icon=icon)

@app.route("/login/operator")
def operator_login():
    icon=url_for("static", filename="icon.svg")
    return render_template("operator_login.html",icon=icon)

@app.route("/user/email", methods=["POST", "GET"])
def get_email():
    if request.method == "POST":
        user_email = request.form["user_email"]
        print(user_email)
        return redirect(url_for("user_qr"))

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
