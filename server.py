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

@app.route('/calendar', methods=['GET'])
#@login-required
def calendar():
    if 'user_id' in session:
        return render_template('caldendar.html')
    else:
        return redirect('/join')

@app.route('/create', methods=['GET', 'POST'])
def create():
#@login_required
    if 'user_id' not in session:
        redirect('/email')

    if request.method == 'POST':
        #somehow render the custom url
        return redirect('/event')
    else:
        return redirect('/register')

@app.route('/email', methods=['POST', 'GET'])
def check_email():
    """Looks for email in users and sends user_id to join route; \
       if email is not in users, redirects to creates account"""

    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        session['user_id'] = user.id

        if user and user.role == 'sundae':
            flash("You've been here before! Let's get you set up")
            return redirect('/join') #, email=user.email) #sends to join

        if user and user.role ==  'user':
            render_template('/VIP-only.html') #, email=user.email) #sends to login

        else:
            user = User(email=email)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return redirect('/join') #, email=user.email) #sends to join

    return render_template('email.html')


@app.route('/exit') #login required
def exit():
    #clear sessions? session[]
    return redirect(url_for('index'))

@app.route('/home') #VIP-only required
def home():
    return render_template('home.html')

@app.route('/intro') #shown after account creation
def intro():
    return render_template('intro.html')

@app.route('/join', methods=['GET', 'POST'])
def join():
    if 'user_id' in session:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            postal_code = request.form.get('postal_code')
            phone = request.form.get('phone')
            role = 'user'

            usr_id = session['user_id']

            db.session.query().\
            filter(User.id == usr_id).\
            update({"username": (username), \
                    "password": (password), \
                    "fname": (fname), \
                    "lname": (lname), \
                    "postal_code": (postal_code), \
                    "phone": (phone), \
                    "role": (role)})
            db.session.commit()

            return redirect('/intro')
        return render_template('/join.html')
    return redirect('/email')

@app.route('/register')
def register_venue():
    return render_template('/register.html')

@app.route('/socials', methods=['GET'])
def show_socials():
    return render_template('/socials.html') #, event_url=url)

@app.route('/RSVP', methods=['GET'])
def RSVP():
    return render_template('/event.html') #, event_url=url)

@app.route('/VIP-only', methods=['POST', 'GET'])
def VIP_only():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            session['user_id'] = user.id
            session['postal_code'] = user.postal_code
            return redirect('/home')
        else:
            return redirect('join.html')
    return render_template('VIP-only.html')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, port=5000, host='0.0.0.0')
