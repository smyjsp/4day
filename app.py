from flask import Flask, render_template, request, redirect, url_for 
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from pytz import timezone

load_dotenv()

app = Flask(__name__)

def send_email(to_email, name, subject="4day", body=None):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email

    if body is None:
        body = f"""
        <html>
            <body style="margin:0; padding:0; font-family: Arial, sans-serif; background-color: #317292; line-height: 1.5;">
                <div style="max-width:600px; margin:20px auto; 
                            border-top:4px solid #333333; 
                            border-bottom:4px solid #333333; 
                            background:white; padding:30px; 
                            text-align:center; 
                            box-shadow:0 0 10px rgba(0,0,0,0.1);">
                    <h1 style="font-size:24px; color:#333333;">Hello {name}, </h1>
                    <p style="font-size:18px; color:#333333; line-height:1.6;">
                        Thanks for signing up! Have a great day! 
                    </p>
                    <p style="margin-top:30px; font-size:14px; color:#333333;">
                        Sincerely, <br>4day</p>
                    <p style="font-size:10px; color:#333333; margin-top:20px;">
                        To unsubscribe, <a href="http://127.0.0.1:5000/unsubscribe?email={to_email}" style="color:#317292;">click here</a></p>
                </div>
            </body>
        </html>
        """
    
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, to_email, msg.as_string())
        print("Email Sent")
    except Exception as e:
        print("Error sending", e)


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
    if not (email.endswith(".com") or email.endswith(".mil") or email.endswith(".edu")):
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
    email = request.args.get("email") or request.form.get("email")

    if email:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        updated_data = [entry for entry in data if entry["email"] != email]

        with open(DATA_FILE, "w") as f:
            json.dump(updated_data, f, indent=4)

        return render_template("unsubscribed.html", email=email)
    
    return render_template("unsubscribe.html")


@app.route("/unsubscribed")
def unsubscribed():
    return render_template("unsubscribed.html")

scheduler = BackgroundScheduler()

def send_holiday_emails():
    today = datetime.now().strftime("%m-%d")
    
    try:
        with open("holidays.json", "r") as f:
            holiday_messages = json.load(f)
    except FileNotFoundError:
        print("holidays.json not found")
        return 

    if today in holiday_messages:
        with open(DATA_FILE, "r") as f:
            users = json.load(f)
        
        for user in users:
            
            body_html = f"""
            <html>
                <body style="margin:0; padding:0; font-family: Arial, sans-serif; background-color: #317292; line-height: 1.5;">
                    <div style="max-width:600px; margin:20px auto; 
                                border-top:4px solid #333333; 
                                border-bottom:4px solid #333333; 
                                background:white; padding:30px; 
                                text-align:center; 
                                box-shadow:0 0 10px rgba(0,0,0,0.1);">
                        <h1 style="font-size:24px; color:#333333;">Good Day! {user['name']},</h1>
                        <p style="font-size:20px; color:#333333; line-height:1.6;">{holiday_messages[today]}</p>
                        <p style="margin-top:30px; font-size:14px; color:#333333;">Sincerely,<br>4day</p>
                        <p style="font-size:10px; color:#333333; margin-top:20px;">
                            To unsubscribe, 
                        <a href="http://127.0.0.1:5000/unsubscribe?email={user['email']}" 
                           style="color:#317292;">click here</a>
                        </p>
                    </div>
                </body>
            </html>
            """
            
            send_email(
                user["email"],
                user["name"],
                subject = "Holiday Greetings from 4day",
                body=body_html
            )

scheduler.add_job(
    send_holiday_emails, 
    "cron", 
    hour=8, 
    minute=0,
    timezone=timezone("US/Eastern"))

scheduler.add_job(send_holiday_emails, "interval", minutes=1) # For testing purpose
scheduler.start()

if __name__ == "__main__":
    send_holiday_emails() # For testing purpose
    app.run(debug=True, use_reloader=False) 
