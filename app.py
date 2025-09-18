from flask import Flask, render_template, request, redirect, url_for 
import json
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def send_email(to_email, name):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEText(f"Hello {name}, \n Test")
    msg["Subject"] = "4day Test"
    msg["From"] = sender
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, to_email, msg.as_string())
        print("Email Sent")
    except Exception as e:
        print("Error", e)


# url_for() must match the function name of the route
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


# Ensure that the data.json file exists
DATA_FILE = "data.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f) # starts with empty list if not found

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")

    # Backend Validation
    if not (email.endswith(".com") or email.endswith(".mil")):
        return render_template("thankyou.html", error="Invalid email domain.", name=name, email=email)

    # Load existing data
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    # Append new entry
    data.append({"name": name, "email": email})

    # Save Data
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent = 4)

    # Send email
    send_email(email, name)
    
    return render_template("thankyou.html", name=name) #key=value without spaces

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

@app.route("/unsubscribe", methods=["GET", "POST"])
def unsubscribe():
    if request.method == "POST":
        email = request.form.get("email")

        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        # keeps the users whos email is NOT the one entered
        updated_data = [entry for entry in data if entry["email"] != email]

        with open(DATA_FILE, "w") as f:
            json.dump(updated_data, f, indent = 4)
        
        return render_template("unsubscribed.html", email=email) #key=value without spaces
    
    return render_template("unsubscribe.html")

@app.route("/unsubscribed")
def unsubscribed():
    return render_template("unsubscribed.html")

if __name__ == "__main__":
    app.run(debug=True)