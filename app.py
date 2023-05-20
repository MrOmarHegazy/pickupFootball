import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask import Flask, g, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import os
from helpers import apology, login_required, lookup, usd
from models import db, User, Field, Slot, Booking, WaitingList
import re

def create_app():
    app = Flask(__name__)

    # Custom filter
    app.jinja_env.filters["usd"] = usd

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    """ Configure SQLite database """
    currentdirectory = os.path.dirname(os.path.abspath(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(currentdirectory, 'registration.db')

    db.init_app(app) #Binds the db object to our Flask app

    return app

app = create_app()

@app.route("/")
@login_required
def index():
    """Show user profile, cash in account, days registered"""
    # TO-DO

    return render_template("index.html")

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

        # Ensure Entry was submitted
        if not request.form.get("login_entry"):
            flash("Must Provide Email or Phone Number!")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must Provide Password!")
            return render_template("login.html")
        
        else:
            loginEntry = request.form.get("login_entry")
            password = request.form.get("password")

        #Process entry, whether email or phone number, then query the database for the user
        if process_input(loginEntry) == "email":
            user = User.query.filter_by(email=loginEntry).first()
          
        elif process_input(loginEntry) == "phone number":
            user = User.query.filter_by(phoneNumber=loginEntry).first()
        
        else:
            flash("Please enter a valid email or phone number!")
            return render_template("login.html")

        # Ensure username exists and password is correct
        if not user:
            return apology("The Email or Phone Number you Provided is not registered. Please register and try again.", 403)
        
        elif not check_password_hash(user.password, password):
            flash("Incorrect Password!")
            return render_template("login.html")

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

        password = request.form.get("password")
        hashed_password = generate_password_hash(password)
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")

        #Validate Input 
        """TO-DO"""

        user = User(password=hashed_password, email=email, phoneNumber=phone_number, firstName=first_name, lastName=last_name)

        try:
            db.session.add(user)
            db.session.commit()
            print("Registration Successful")
        except IntegrityError as e:
            db.session.rollback()
            print(str(e.orig))
            flash('Username, email, or phone number already exist!')
            print("Integrity Error")
            return redirect('/register')  # Replace with the registration page

        # Proceed as normal...
        return render_template("registration_success.html")  # Replace with the success page

    else:
        return render_template("register.html")
    
@app.route("/book")
@login_required
def book():
    return
    
def process_input(user_input):
    # Regex pattern for email
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    # Regex pattern for phone number
    phone_regex = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')

    if email_regex.fullmatch(user_input):
        return "email"
    elif phone_regex.fullmatch(user_input):
        return "phone number"
    else:
        return "invalid"

if __name__ == "__main__":

    """All this code only works when you run "python app.py" for example directly, but when running flask, you import this file as a module, and so all this code below never runs"""

    with app.app_context():
        db.create_all()
        print("Database Table Created")
    app.config['DEBUG'] = True                     #Only for developement
    app.config['TEMPLATES_AUTO_RELOAD'] = True     #Only for developement
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0    #Removes cache, only for dev
    app.run()