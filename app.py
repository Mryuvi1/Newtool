from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, requests

app = Flask(__name__)
app.secret_key = "your_secret_key"

def get_user(username):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT username, password, approved FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()
    return user

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = get_user(username)
        if user and user[1] == password:
            if user[2]:
                session["user"] = username
                return redirect("/dashboard")
            else:
                return render_template("pending.html")
        else:
            return "Invalid credentials"
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    token_result = None
    if request.method == "POST":
        cookies = request.form["cookies"]
        headers = {"Cookie": cookies}
        res = requests.get("https://business.facebook.com/business_locations", headers=headers)
        token = None
        if "EAAG" in res.text:
            token = res.text.split("EAAG")[1].split('"')[0]
            token = "EAAG" + token
            token_result = token
        else:
            token_result = "Token not found or cookies invalid."

    return render_template("dashboard.html", token=token_result)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")