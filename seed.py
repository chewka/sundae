from sqlalchemy import func
from model import Category, User, Venue, Event, Category_Subcategory

from server import app
from model import connect_to_db, db
from datetime import datetime

def load_categories():
    """Load venue categories into database"""

    print('load_categories')

    Category.query.delete()

    for row in open("seed_data/categories.csv"):
        row = row.rstrip()
        name = row.split(',')


        cat = Category(name=name)

        db.session.add(cat)

    db.session.commit()


def load_subcategories():
    """Load venue subcategories into database"""

    print('load_subcategories')

    Category_Subcategory.query.delete()

    for row in open("seed_data/subcategories.csv"):
        row = row.rstrip()
        category_id, name = row.split(',')


        sub = Category_Subcategory(main_category=category_id,
                            name=name)

        db.session.add(sub)

    db.session.commit()


def load_sundaes():
    """Load 'ghost' users (aka 'sundaes') into database"""

    print('load_sundaes')

    User.query.delete()

    for row in open("seed_data/sundaes.csv"):
        row = row.rstrip()
        email, postal_code = row.split(',')


        usr = User(email=email,
                   postal_code=postal_code)

        db.session.add(usr)

    db.session.commit()


def load_users():
    """Load signed-up users into database"""

    print('load_users')

    for row in open("seed_data/users.csv"):
        row = row.rstrip()

        email, \
        postal_code, \
        fname, \
        lname, \
        username, \
        password, \
        phone, \
        role = row.split(',')


        usr = User(email=email,
                   postal_code=postal_code,
                   fname=fname,
                   lname=lname,
                   username=username,
                   password=password,
                   phone=phone,
                   role=role)

        db.session.add(usr)

    db.session.commit()


def load_venues():
    """Load venue information into database"""

    print('load_venues')

    Venue.query.delete()

    for row in open("seed_data/venues.csv"):
        row = row.rstrip()
        subcategory, \
        title, \
        addr_1, \
        addr_2, \
        city, \
        postal_code, \
        state = row.split(',')

        cat_sub = Category_Subcategory.query.filter_by(name=subcategory).first()

        vnu = Venue(subcategory_id=cat_sub.id,
                   name=title,
                   addr_1=addr_1,
                   addr_2=addr_2,
                   city=city,
                   postal_code=postal_code,
                   state=state)

        db.session.add(vnu)

    db.session.commit()

def load_events():
    """Load events into database"""

    print('load_events')

    Event.query.delete()

    for row in open("seed_data/events.csv"):
        row = row.rstrip()
        private, \
        host_id, \
        venue, \
        title, \
        time_begin, \
        time_end, \
        max_cap, \
        url = row.split(',')

        private = int(private)
        host_id = int(host_id)

        ven = Venue.query.filter_by(name=venue).first()

        begin_at = datetime.strptime(time_begin, "%y-%m-%d %H:%M:%S")

        end_at = datetime.strptime(time_end, "%y-%m-%d %H:%M:%S")

        evt = Event(private=private,
                   host_id=host_id,
                   venue_id=ven.id,
                   title=title,
                   begin_at=begin_at,
                   end_at=end_at,
                   max_cap=max_cap,
                   url=url)

        db.session.add(evt)

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_categories()
    load_subcategories()
    load_sundaes()
    load_users()
    load_venues()
    load_events()
