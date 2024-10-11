import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

@app.route('/')
def test():
    return render_template("temp.html")

@app.route('/register')
def register():
    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)
