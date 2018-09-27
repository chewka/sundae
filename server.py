"""Sundae Socials: get together"""
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
#from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from model import User, Venue, Event, Category, connect_to_db, db

app = Flask(__name__)
app.secret_key = "ABC"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            session['user'] = user.id
            session['zip_code'] = user.zip_code
            return render_template('home.html')
        else:
            return redirect('create-account.html')

        print(message)
    return render_template('login.html')


@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        zip_code = request.form.get('zip_code')
        phone = request.form.get('phone')
        role = 'user'

        if User.query.filter_by(email=email).first():
            flash("This email is already in use")
            return redirect('/create-account')

        else:
            user = User(username=username,
                        password=password,
                        fname=fname,
                        lname=lname,
                        email=email,
                        zip_code=zip_code,
                        phone=phone,
                        role=role)

            db.session.add(user)
            db.session.commit()

            return render_template('intro.html')

    return render_template('create-account.html')

@app.route('/intro') #login required
def intro():
    return render_template('intro.html')

@app.route('/home') #login required
def home():
    return render_template('home.html')

@app.route('/logout') #login required
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, port=5000, host='0.0.0.0')
