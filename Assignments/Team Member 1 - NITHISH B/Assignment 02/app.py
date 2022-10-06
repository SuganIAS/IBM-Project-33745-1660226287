from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def homepage():
    return render_template('home.html')

@app.route("/about")
def aboutpage():
    return render_template('about.html')

@app.route("/signin")
def signinpage():
    return render_template('signin.html')

@app.route("/signup")
def signuppage():
    return render_template('signup.html')