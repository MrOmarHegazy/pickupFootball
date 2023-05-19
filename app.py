import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, g, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import os
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)
currentdirectory = os.path.dirname(os.path.abspath(__file__))

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

""" Configure SQLite database """

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////registration.db'  
db = SQLAlchemy(app) #Initialize App

#First Table "Users" of registration.db database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstName = db.Column(db.String(80), unique=True, nullable=False)
    lastName = db.Column(db.String(80), unique=True, nullable=False)
    cashBalance = db.Column(db.Integer)

    #posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

# Create an application context
with app.app_context():
    # After defining your models, create the tables
    db.create_all()
###########################################################################

@app.route("/")
@login_required
def main():
    """Show user profile, cash in account, days registered"""
    # TO-DO

    return apology("TO-DO", 400)
    #return render_template("index.html")

@app.route("/calendar", methods=["GET", "POST"])
def calendar():
    return render_template("calendar.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must Provide Username!")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must Provide Password!")
            return render_template("login.html")
        
        else:
            username = request.form.get("username")
            password = request.form.get("password")

        # Query the database directly for the user by username
        user = User.query.filter_by(username=username).first()  


         # Ensure username exists and password is correct
        if not user or not check_password_hash(user.password, password):
            # This means either the user wasn't found, or the password was incorrect.
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password)

        # """Validate Input"""
        # db = get_db()
        # cursor = db.cursor()
        # query1 = "SELECT * FROM users WHERE username = ?"
        # usernames = cursor.execute(query1, (username,))

        # if username == "":
        #     return apology("Please enter a username", 400)

        # elif len(usernames) > 0:
        #     return apology("Username already exists", 400)

        # else:
        #     query1 = "INSERT INTO users (username, hash) VALUES(?, ?)"
        #     cursor.execute(query1, (username, hashed_password))
        #     connection.commit()

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")
    
if __name__ == '__main__':
    #app.config[‘TEMPLATES_AUTO_RELOAD’] = True
    #app.config[‘SEND_FILE_MAX_AGE_DEFAULT’] = 0
    app.run() 
