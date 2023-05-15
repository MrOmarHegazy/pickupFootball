import sqlite3
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
currentdirectory = os.getcwd()  # get current directory
db_path = os.path.join(currentdirectory, "registration.db")  # join path

# check if the directory exists
if not os.path.exists(currentdirectory):
    print(f"Directory {currentdirectory} does not exist")

# check if you have write permissions in this directory
if not os.access(currentdirectory, os.W_OK):
    print(f"No write permission in the directory {currentdirectory}")

# Now try to connect to the database
try:
    connection = sqlite3.connect(db_path)
except sqlite3.OperationalError as e:
    print(f"Couldn't open the database at {db_path}. Error: {e}")

# The following three functions are intended to make the database start a new object everytime a connection wats to be used
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_path)
    return db

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
###############################################################################

@app.route("/")
@login_required
def main():
    """Show available days on a calendar"""
    # TO-DO

    return apology("TO-DO", 400)
    #return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        db = get_db()
        cursor = db.cursor()
        query1 = "SELECT * FROM users WHERE username = ?", (request.form.get("username"),)
        rows = cursor.execute(query1).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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

        """Validate Input"""
        query1 = "SELECT * FROM users WHERE username LIKE {n}".format(n = username )

        # Create new connection and cursor
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        usernames = cursor.execute(query1)
        connection.commit()

        # Close connection
        connection.close()

        if username == "":
            return apology("Please enter a username", 400)

        elif len(usernames) > 0:
            return apology("Username already exists", 400)

        else:
            # Create new connection and cursor
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            query1 = "INSERT INTO users (username, hash) VALUES({usrn}, {hpass})".format(usrn = username, hpass = hashed_password )
            cursor.execute(query1)
            connection.commit()

            # Close connection
            connection.close()

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")
    
if __name__ == '__main__':
    app.debug = True  #This updates browser with every code change, and gives useful tips if things go wrong
    app.run()
