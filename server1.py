"""Sundae Socials: get together"""
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, url_for
#from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/home') #login required
def home():
    return render_template('home.html')

@app.route('/logout') #login required
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
#
#
#
#          <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
#          <a class="dropdown-item" href="/hosting">hosting</a>
#          <a class="dropdown-item" href="/attending">attending</a>
#          <a class="dropdown-item" href="/interested">interested</a>
#          <a class="dropdown-item" href="/invited">invited</a>
#          <a class="dropdown-item" href="/confirmed">confirmed</a>
