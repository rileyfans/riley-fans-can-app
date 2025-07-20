from flask import Flask, render_template, request, redirect, flash, session, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("ADMIN_PASSWORD", "David452")

CARD_DIR = "fan_cards"
os.makedirs(CARD_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        amount = request.form["amount"]

        card_path = os.path.join(CARD_DIR, f"{name}_{datetime.now().timestamp()}.txt")
        with open(card_path, "w") as f:
            f.write(f"Name: {name}\nEmail: {email}\nAmount: {amount}\n")

        flash("Thank you! Your donation was received, and your fan card was created!")
        return redirect("/")

    return render_template("donate.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form["password"]
        if password == app.secret_key:
            session["admin"] = True
            return redirect("/admin")
        else:
            flash("Incorrect password")
    return render_template("login.html")


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/admin/login")

    cards = os.listdir(CARD_DIR)
    return render_template("admin.html", cards=cards)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
    
@app.route("/fan_cards/<filename>")
def get_card(filename):
    return send_from_directory(CARD_DIR, filename)
