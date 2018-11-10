"""Sundae Socials: get together"""
from jinja2 import StrictUndefined
from functools import wraps
from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, request, flash, session, g, jsonify
from flask_sqlalchemy  import SQLAlchemy
#from werkzeug.security import generate_password_hash, check_password_hash
from model import User, Venue, Event, Category, connect_to_db, db, Invited

app = Flask(__name__)
app.secret_key = "ABC"

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect('/join')
        return f(*args, **kwargs)
    return decorated_function

def already_loggedin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id'):
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    today = datetime.now()
    #print(today)
    today = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    events_today = Event.query.filter(Event.begin_at>=today, Event.end_at<=tomorrow, Event.private==False).order_by(Event.begin_at).all()

    this_month = today + timedelta(days=31)
    #print (this_month - today)
    events_upcoming = Event.query.filter(Event.begin_at>=today, Event.end_at<=this_month).order_by(Event.begin_at).all()

    return render_template('index.html', events_today=events_today, events_upcoming=events_upcoming)


@app.route('/categories_subcategories', methods=['GET'])
def get_subcategories():
    venues = Venue.query.filter_by(Venue.country=='United States').all()
    return jsonify(venues)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        info = request.form.get('info')

        begin_time = request.form.get('begin_time')
        begin_date = request.form.get('begin_date')
        begin_at = datetime.strptime(begin_date + ' ' + begin_time, "%m/%d/%Y %I:%M %p")
        end_time = request.form.get('end_time')
        end_date = request.form.get('end_date')
        end_at = datetime.strptime(end_date + ' ' + end_time, "%m/%d/%Y %I:%M %p")
        max_cap = request.form.get('max_cap')
        if max_cap == '':
            max_cap = 1
        url = request.form.get('url')

        #if url is unique to the host --proceed; if not: choose another name

        private_html = request.form.get('private')
        if private_html == 'True':
            private = True
        else:
            private = False
        venue_name = request.form.get('venue')

        venue = Venue.query.filter_by(name=venue_name).first()
        venue_id = venue.id

        host_id = session['user_id']
        #venue_id = session['venue_id']
        #Drop-down instead of storing in session

        event = Event(title=title, \
                      info=info, \
                      begin_at=begin_at, \
                      end_at=end_at, \
                      max_cap=max_cap, \
                      url=url, \
                      private=private, \
                      host_id=host_id, \
                      venue_id=venue_id)

        db.session.add(event)
        db.session.commit()

        session.pop('venue_id', None)

        #session['event_id'] = event.id

        return redirect('/event/{}/{}'.format(event.host_id, event.url)) #, event_url=event_url)

    venues = Venue.query.order_by(Venue.name).all()
    #flash(venues)
    return render_template('/create.html', venues=venues)

@app.route('/email', methods=['POST', 'GET'])
@already_loggedin
def check_email():
    """Looks for email in users and sends user_id to join route; \
       if email is not in users, redirects to creates account"""

    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user and user.role == 'sundae':
            flash("User account created! Add more info!")
            session['user_id'] = user.id
            return redirect('/join') #, email=user.email) #sends to join

        if user and user.role ==  'user':
            email = user.email
            session['user_id'] = user.id
            return redirect('/VIP-only') # email=email) #sends to login

        else:
            user = User(email=email)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            email = user.email
            return redirect('/join') #, email=email) #sends to join

    return render_template('email.html')

@app.route('/event/<host_id>/<event_url>') #VIP-only login
def show_event(host_id, event_url):
    event = Event.query.filter_by(url=event_url).one()
    venue = Venue.query.filter_by(id=event.venue_id).first()
    #venue = event.venue_id

    #private = event.private
    #if event = private, then find user id if logged in;
    #if not logged in, ask for email confirmation
    #user_id = session['user_id']

    #NEXT: CREATE INVITE LIST

    #not logged in, have to give us email; session['user_id']

    #if private == True and event.invites.filter_by(user_id=user_id)
        #return render_template()

    title = event.title
    begin_at = event.begin_at
    end_at = event.end_at
    if event.info:
        info = event.info
    else:
        info = ''
    max_cap = event.max_cap
    url = event.url
    host_id = event.host_id

    #if user is host:
        #show invite button --> take to a different page

    return render_template('event.html', title=title, \
                                         info=info, \
                                         venue=venue, \
                                         begin_at=begin_at, \
                                         end_at=end_at, \
                                         url=url, \
                                         host_id=host_id)

                                         ##BLOCKKED!!

@app.route('/exit') #login required
def exit():
    #clear sessions? session[]
    session.pop('user_id', None)
    return redirect('/')

@app.route('/intro') #shown after account creation
def intro():
    return render_template('intro.html')

@app.route('/invite/<user_id>/<event_url>', methods=['GET']) #shown after event creation
def invite_get(user_id, event_url):
    event = Event.query.filter_by(url=event_url).one()
    max_cap = event.max_cap
    return render_template('invite.html', user_id=user_id, event_url=event_url, max_cap=max_cap)

@app.route('/invite/<user_id>/<event_url>', methods=['POST']) #shown after event creation
def invite_post(user_id, event_url):
    user = User.query.get(user_id)
    print(user.invites)
    event = Event.query.filter_by(url=event_url, host_id=user_id).first()
    #email_invites = []
    # for i in event.max_cap:
    #     invite_email = request.form.get('email {}'.format(i))
    #     email_invites.append(invite_email)
    #     for email in email_invites:
    #         user = User(email=email)
    #         db.session.add(user)
    #         db.session.commit()
    #         invited = Invited(user_id=user.id, \
    #                           event_id=event.id, \
    #                           invited_at = datetime.datetime.now())

    csv_emails = request.form.get('csv_emails')
    invite_emails = csv_emails.replace(' ','').rstrip().split(',')
    for email in invite_emails:
        user = User.query.filter_by(email=email).first()
        # for item in user.invites:
        #     if event.id != item.event_id:
                #iterate through list: if user.invites != event.id:
                #invited filter by user id and event id;

        if user is None:
            user = User(email=email)
            db.session.add(user)
            db.session.commit()

        invited = Invited(user_id=user.id, \
                          event_id=event.id, \
                          invited_at=datetime.now())
        db.session.add(invited)
        db.session.commit()

        event = Event.query.filter_by(id=invited.event_id).first()
        # last_email = Event.query.filter_by(id=invited.event_id).order_by("Invited."id.desc()).first()

    return render_template('invited.html', invite_emails=invite_emails, event=event)


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

            user_id = session['user_id']
            user = User.query.get(user_id)

            if User.query.filter_by(username=username).first():
                flash("username already exists, please try again")
            else:
                user.username = username
                user.password = password
                user.fname = fname
                user.lname = lname
                user.postal_code = postal_code
                user.phone = phone
                user.role = 'user'

                db.session.commit()

                return redirect('/intro')
            return render_template('/join.html', fname=fname, \
                                                 lname=lname, \
                                                 postal_code=postal_code, \
                                                 phone=phone)
        return render_template('/join.html')
    return redirect('/email')

@app.route('/me', methods=['GET'])
@login_required
def show_profile():
    user_id = session['user_id']
    user = User.query.get(user_id)

    username = user.username
    fname = user.fname
    lname = user.lname
    email = user.email
    postal_code = user.postal_code
    phone = user.phone

    return render_template('/me.html', username=username,\
                                  fname=fname, \
                                  lname=lname, \
                                  email=email, \
                                  postal_code=postal_code)

@app.route('/register', methods=['GET'])
@login_required
def show_register_venue():
    return render_template('/register.html')

@app.route('/register', methods=['POST'])
@login_required
def register_venue():

    name = request.form.get('name')
    addr_1 = request.form.get('addr_1')
    addr_2 = request.form.get('addr_2')
    city = request.form.get('city')
    postal_code = request.form.get('postal_code')
    state = request.form.get('state')
    country = request.form.get('country')
    category = request.form.get('category')

    if Venue.query.filter_by(name=name).first():
        return jsonify({'error' : 'duplicate name'})

    user_id = session['user_id']
    user = User.query.get(user_id)
    created_by = user.id

    venue = Venue(name=name, \
                  addr_1=addr_1, \
                  addr_2=addr_2, \
                  city=city, \
                  postal_code=postal_code, \
                  state=state, \
                  country=country, \
                  created_by=created_by)

    db.session.add(venue)
    db.session.commit()

    session['venue_id'] = venue.id

    return redirect('/create')


@app.route('/socials', methods=['GET'])
@login_required
def show_socials():
    #hosting: find the user, find where the user and the host ID are the same
    user_id = session['user_id']
    user = User.query.get(user_id)
    user_id = user.id

    invited = Invited.query.filter_by(user_id=user_id).all()

    hosting = Event.query.filter_by(host_id=user_id).order_by(Event.begin_at).all()

    return render_template('/socials.html', user_id=user_id, invited=invited, hosting=hosting) #, event_url=url)

@app.route('/RSVP', methods=['GET'])
def RSVP():
    return render_template('/event.html') #, event_url=url)

@app.route('/venues', methods=['GET'])
def venues():
    venues = Venue.query.filter_by(country='United States')
    return render_template('/venues.html', venues=venues)

@app.route('/VIP-only', methods=['POST', 'GET'])
def VIP_only():
    user_id = session['user_id']
    user = User.query.get(user_id)
    email = user.email
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if user.password == password and user.email == email:
            session['user_id'] = user.id
            return redirect('/')
        else:
            flash("password does not match")
            return redirect('/VIP-only')
    return render_template('VIP-only.html', email=email)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, port=5000, host='0.0.0.0')
