"""Models and database functions for Sundae db."""

from flask_sqlalchemy import SQLAlchemy

# Here's where we create the idea of our database. We're getting this through
# the Flask-SQLAlchemy library. On db, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


class Users(db.Model):
    """Users model."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(22), unique=True, index=True, nullable=False)
    password = db.Column(db.String(22), nullable=True)
    fname = db.Column(db.String(22), nullable=True)
    lname = db.Column(db.String(22), nullable=True)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    postal_code = db.Column(db.String(12), nullable=True)
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


class Events(db.Model):
    """Events model."""

    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    postal_code = db.Column(db.String(12), nullable=True)


    human = db.relationship('Human', backref='animals')

    def __repr__(self):

        return f"<Animal animal_id={self.animal_id} human_id={self.human_id} name={self.name} animal_species={self.animal_species} birth_year={self.birth_year}>"


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
