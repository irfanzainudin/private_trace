from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/user")
def user_login():
    icon="./static/icon.svg"
    return render_template("user_login.html",icon=icon)

if __name__ == "__main__":
    app.run(debug=True)