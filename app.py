import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology
from functools import wraps

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database connection
db = SQL("sqlite:///resourceNation.db")

# Create the users table if it doesn't exist
db.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL
    )
    """
)


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def test():
    return render_template("layout.html", css_file="css/styles.css")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Check if username exists and if password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html", css_file="css/styles2.css")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirm_password"):
            return apology("must confirm password", 400)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirm_password"):
            return apology("passwords do not match", 400)

        # Check if username already exists
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) > 0:
            return apology("username already exists", 400)

        # Hash the password
        hash_password = generate_password_hash(request.form.get("password"))

        # Insert the new user into the database
        result = db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            request.form.get("username"),
            hash_password,
        )
        if not result:
            return apology("registration failed", 400)

        # Log the user in by storing the user_id in the session
        user_id = db.execute(
            "SELECT id FROM users WHERE username = ?", request.form.get("username")
        )
        session["user_id"] = user_id[0]["id"]

        return redirect("/")
    else:
        return render_template("register.html", css_file="css/styles2.css")


@app.route("/courses", methods=["POST", "GET"])
@login_required
def courses():
    if request.method == "POST":
        pass
    else:
        return render_template("courses.html", css_file="css/styles3.css")


@app.route("/courses/<course_name>")
@login_required
def course(course_name):
    # Path to the course-specific folder inside the "pdfs" directory
    course_dir = os.path.join("static", "pdfs", course_name)

    # Check if the directory exists
    if not os.path.exists(course_dir):
        return apology("Course not found", 404)

    # Get the list of PDF files in the directory
    pdf_files = [file for file in os.listdir(course_dir) if file.endswith(".pdf")]

    return render_template("course.html", course_name=course_name, pdf_files=pdf_files, css_file="css/courseStyles.css")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
