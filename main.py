from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login/user")
def user_login():
    icon=url_for("static", filename="icon.svg")
    return render_template("user_login.html",icon=icon)

@app.route("/login/operator")
def operator_login():
    icon=url_for("static", filename="icon.svg")
    return render_template("operator_login.html",icon=icon)

if __name__ == "__main__":
    app.run(debug=True)
