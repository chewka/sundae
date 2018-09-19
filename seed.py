from sqlalchemy import func
from model import Category_Subcategory
from model import Category

from model import connect_to_db, db
from server import app


def load_categories():
    """Load venue categories into database"""

    Category.query.delete()

    for row in open("/categories.csv"):
        row = row.rstrip()
        category_id, category = row.split(',')


        cat = Category_Subcategory(id=category_id,
                            category=name)

        db.session.add(cat)

    db.session.commit()


def load_subcategories():
    """Load venue subcategories into database"""

    Category_Subcategory.query.delete()

    for row in open("/subcategories.csv"):
        row = row.rstrip()
        category_id, subcategory = row.split(',')


        sub = Category_Subcategory(id=category_id,
                            subcategory=name)

        db.session.add(sub)

    db.session.commit()


def load_sundaes():
    """Load 'ghost' users (aka 'sundaes') into database"""

    User.query.delete()

    for row in open("/sundaes.csv"):
        row = row.rstrip()
        email, postal_code = row.split(',')


        usr = User(email=email,
                   postal_code=postal_code)

        db.session.add(usr)

    db.session.commit()


def load_users():
    """Load signed-up users into database"""

    for row in open("/users.csv"):
        row = row.rstrip()
        email, 
        postal_code, 
        fname, 
        lname, 
        username, 
        password,
        phone = row.split(',')


        usr = User(email=email,
                   postal_code=postal_code,
                   fname=fname,
                   lname=lname,
                   username=username,
                   password=password,
                   phone=phone)

        db.session.add(usr)

    db.session.commit()


def load_venues():
    """Load venue subcategories into database"""

    Venue.query.delete()

    for row in open("/venues.csv"):
        row = row.rstrip()
        email, postal_code = row.split(',')


        usr = User(email=email,
                   postal_code=postal_code)

        db.session.add(usr)

    db.session.commit()

def load_events():
    """Load events into database"""

    Event.query.delete()

    for row in open("/events.csv"):
        row = row.rstrip()
        private,
        host_id,
        venue,
        title, 
        begin_at,
        end_at,
        max_cap,
        url = row.split(',')


        evt = User(private=private,
                   host_id=host_id,
                   venue=venue,
                   title=title,
                   begin_at=begin_at,
                   end_at=end_at,
                   max_cap=max_cap,
                   url=url)

        db.session.add(evt)

    db.session.commit()