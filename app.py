from flask import Flask, render_template, request, redirect, url_for 
import json
import os

app = Flask(__name__)

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

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    data.append({"name": name, "email": email})

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
    
    return redirect(url_for("thankyou"))

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

if __name__ == "__main__":
    app.run(debug=True)