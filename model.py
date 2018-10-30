"""Models and database functions for Sundae db."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# User: indexed by 'email' and by 'id'
# User: required values = email, postal_code, role (default='user'), authorized (default=True)
# Venues: indexed by 'name'
# Venues: required values = name, category, postal_code, country (default='United States')
# Events: indexed by 'begin_at'
# Events: required values = all except 'max_cap'
# To create a user: only need an email and zip code

# Emails + Events = Invited, Interested, Confirmed

# Once a user marks 'Yes' for attending, they will be added to 'Confirmed' table
# Does not need to be a user to mark 'Yes'
# Interested = if marked 'Maybe')
# Does not need to be a user to mark 'Maybe'
# Invited = if added to invite list

# interested || invited < confirmed

db = SQLAlchemy()


class User(db.Model):
    """Users model."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(22), unique=True, nullable=True)
    password = db.Column(db.String(22), nullable=False, default="nadamucho")
    fname = db.Column(db.String(22), nullable=True)
    lname = db.Column(db.String(22), nullable=True)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    postal_code = db.Column(db.String(12), nullable=True, default=94710)
    phone = db.Column(db.String(15), unique=False, nullable=True)
    role = db.Column(db.String(15), default='sundae', nullable=False) #permissions: admin, host, user
    authorized = db.Column(db.Boolean, default=True, nullable=False) #security: protect against blocked users

    # @classmethod
    # def check_user(cls, prop):
    #     return cls.query.filter_by(email=prop).first()

    def __repr__(self):
        repr_str = '<User: \
                    id={} \
                    username={} \
                    password={} \
                    fname={} \
                    lname={} \
                    email={} \
                    postal_code={} \
                    phone={} \
                    role={} \
                    authorized={}>'

        return repr_str.format(
                    self.id,
                    self.username,
                    self.password,
                    self.fname,
                    self.lname,
                    self.email,
                    self.postal_code,
                    self.phone,
                    self.role,
                    self.authorized)


class Category(db.Model):
    """Categories that users can choose from for venues"""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    img = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        repr_str = '<Category: \
                    id={}, \
                    name={}, \
                    img={}>'


        return repr_str.format(
                    self.id,
                    self.name,
                    self.img)


class Category_Subcategory(db.Model):
    """Categories that users can choose from for events, venues, or topics"""

    __tablename__ = 'categories_subcategories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    main_category = db.Column(db.Integer, db.ForeignKey('categories.id'))
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        repr_str = '<Category_Subcategory: \
                    id={}, \
                    main_category={}, \
                    name={}>'


        return repr_str.format(
                    self.id,
                    self.main_category,
                    self.name)


class Venue(db.Model):
    """Venues model."""

    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('categories_subcategories.id'), nullable=True) #User prompts info in form: house, bar, park, nightclub, etc.
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), unique=True, index=True, nullable=False)
    addr_1 = db.Column(db.String(100), nullable=True)
    addr_2 = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    postal_code = db.Column(db.String(12), nullable=False)
    state = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), default='United States', nullable=False)

    def __repr__(self):
        repr_str = '<User: \
                    id={} \
                    subcategory_id={} \
                    created_by={} \
                    name={} \
                    addr_1={} \
                    addr_2={} \
                    city={} \
                    postal_code={} \
                    state={} \
                    country={}>'

        return repr_str.format(
                    self.id,
                    self.subcategory_id,
                    self.created_by,
                    self.name,
                    self.addr_1,
                    self.addr_2,
                    self.city,
                    self.postal_code,
                    self.state,
                    self.country)


class Event(db.Model):
    """Events model."""

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    private = db.Column(db.Boolean, default=False, nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id')) # Form prompts adding venue or searching for venue before creating event
    title = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(500), nullable=True)
    begin_at = db.Column(db.DateTime, nullable=False, index=True) # YYYY-MM-DD HH:MI:SS
    end_at = db.Column(db.DateTime, nullable=False) # YYYY-MM-DD HH:MI:SS
    max_cap = db.Column(db.Integer, nullable=True)
    url = db.Column(db.String(100), unique=True, nullable=False, index=True)

    def __repr__(self):
        repr_str = '<User: \
                    id={} \
                    private={} \
                    host_id={} \
                    venue_id={} \
                    title={} \
                    info={} \
                    begin_at={} \
                    end_at={} \
                    max_cap={} \
                    url={}'

        return repr_str.format(
                    self.id,
                    self.private,
                    self.host_id,
                    self.venue_id,
                    self.title,
                    self.info,
                    self.begin_at,
                    self.end_at,
                    self.max_cap,
                    self.url)

class Invited(db.Model):
    """Events users have been invited to an event"""

    __tablename__ = 'invites'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    invited_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref='invites')
    event = db.relationship('Event', backref='invites')

    def __repr__(self):
        repr_str = '<Invited: \
                    id={}, \
                    user_id={}, \
                    event_id={}, \
                    invited_at={}>'

        return repr_str.format(
                    self.id,
                    self.user_id,
                    self.event_id,
                    self.invited_at)


class Interested(db.Model):
    """Events users have marked 'Maybe'"""

    __tablename__ = 'interests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    interested_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref='interests')
    event = db.relationship('Event', backref='interests')

    def __repr__(self):
        repr_str = '<Interested: \
                    id={}, \
                    user_id={}, \
                    event_id={}, \
                    interested_at={}>'

        return repr_str.format(
                    self.id,
                    self.user_id,
                    self.event_id,
                    self.interested_at)


class Confirmed(db.Model):
    """Events users have confirmed a 'Yes' response"""

    __tablename__ = 'confirms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    confirmed_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref='confirms')
    event = db.relationship('Event', backref='confirms')

    def __repr__(self):
        repr_str = '<Confirmed: \
                    id={}, \
                    user_id={}, \
                    event_id={}, \
                    invited_at={}>'

        return repr_str.format(
                    self.id,
                    self.user_id,
                    self.event_id,
                    self.invited_at)


def init_app():

    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")


def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///sundae'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    init_app()
