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
