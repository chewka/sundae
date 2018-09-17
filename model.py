"""Models and database functions for Sundae db."""

from flask_sqlalchemy import SQLAlchemy

# User: indexed by 'email' and by 'id'
# User: required values = email, postal_code, role (default='user'), authorized (default=True)
# Venues: indexed by 'name'
# Venues: required values = name, category, postal_code, country (default='United States')
# Events: indexed by ''
# To create a user: only need an email
#

# Emails + Events = Events + Yes + Invited
# Once a user marks 'Yes' for attending, they will be added to 'Invited' table
# Does not need to be a user to mark 'Yes'
# Interested = Events + Email (if marked 'Maybe')
# Does not need to be a user to mark 'Maybe'

db = SQLAlchemy()


class Users(db.Model):
    """Users model."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)

    username = db.Column(db.String(22), unique=True, nullable=True)
    password = db.Column(db.String(22), nullable=True)
    fname = db.Column(db.String(22), nullable=True)
    lname = db.Column(db.String(22), nullable=True)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    postal_code = db.Column(db.String(12), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=True)

    role = db.Column(db.String(15), default='user', nullable=False) #permissions: admin, host, user
    authorized = db.Column(db.Boolean, default=True, nullable=False) #security: protect against blocked users

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


class Venues(db.Model):
    """Venues model."""

    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)

    category = db.Column(db.String(22), nullable=False) #User prompts info in form: house, bar, park, nightclub, etc.

    name = db.Column(db.String(50), unique=True, index=True, nullable=False)
    addr_1 = db.Column(db.String(100), unique=True, nullable=True)
    addr_2 = db.Column(db.String(100), unique=True, nullable=True)
    city = db.Column(db.String(50), nullable=True)
    postal_code = db.Column(db.String(12), nullable=False)
    state = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), default='United States', nullable=False)


    def __repr__(self):

        repr_str = '<User: \
                    id={} \
                    category={} \
                    name={} \
                    addr_1={} \
                    addr_2={} \
                    city={} \
                    postal_code={} \
                    state={} \
                    country={}>'

        return repr_str.format(
                        self.id,
                        self.category
                        self.name,
                        self.addr_1,
                        self.addr_2,
                        self.city,
                        self.postal_code,
                        self.state,
                        self.country)


class Categories(db.Model):
    """Categories that users can choose from for events, venues, or tpics"""

    __tablename__ = 'category'





class Events(db.Model):
    """Events model."""

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)

    private = db.Column(db.Boolean, default=False, nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    venue = db.Column(db.String(50), db.ForeignKey('venues.id')) #Form prompts adding venue or searching for venue before creating event
    title = db.Column(db.String(100), nullable=False)
    begin_at = db.Column(db.DateTime, nullable=False)
    end_at = db.Column(db.DateTime, nullable=False)
    max_cap = db.Column(db.String(50), nullable=True)


        def __repr__(self):

        repr_str = '<User: \
                    id={} \
                    private={} \
                    host_id={} \
                    venue={} \
                    title={} \
                    begin_at={} \
                    end_at={} \
                    max_cap={}'

        return repr_str.format(
                        self.id,
                        self.private,
                        self.host_id,
                        self.venue,
                        self.title,
                        self.begin_at,
                        self.end_at,
                        self.max_cap)

class Invited(db.Model):
    """Events users have RSVP'd or confirmed 'Yes'"""

    __tablename__ = 'invited'


class Interested(db.Model):
    """Events users have marked 'Maybe'"""

    __tablename__ = 'interested'



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
