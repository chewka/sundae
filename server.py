"""Sundae Socials: get together"""
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
#from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from model import User, Venue, Event, Category, connect_to_db

app = Flask(__name__)
app.secret_key = "ABC"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            session['user'] = user.id
            return render_template('home.html')
        else:
            return redirect('signup.html')

        print(message)
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
    connect_to_db(app)
    app.run(debug=True, port=5000, host='0.0.0.0')
