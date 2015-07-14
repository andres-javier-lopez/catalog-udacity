#coding: utf-8

import sqlalchemy as sqla
from sqlalchemy import orm
from sqlalchemy.ext import declarative

Base = declarative.declarative_base()


class Category(Base):
    """Table that contains the catalog categories.
    """

    __tablename__ = 'categories'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(100), nullable=False)
    items = orm.relationship('Item', backref="category")

class Item(Base):
    """Table that contains the items from the catalog.

    Atrributes:
        id: primary key of the item
        name: name of the item
    """

    __tablename__ = 'catalog'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(100), nullable=False)
    category_id = sqla.Column(sqla.ForeignKey('categories.id'), nullable=False)


def get_engine():
    '''Creates the engine that will be used with the database.'''
    engine = sqla.create_engine('sqlite:///catalog.sqlite')
    return engine


def get_session():
    '''Get a database session that will be used to interact with it.'''
    engine = get_engine()
    DBSession = orm.sessionmaker(bind=engine)
    return DBSession()


def create_database():
    '''Creates all the tables on the database.'''
    engine = get_engine()
    Base.metadata.create_all(engine)


def fill_default_data():
    '''Adds default data to de database.'''
    db_session = get_session()
    default_items = ['red', 'blue', 'black', 'yellow', 'green']

    new_category = Category(name='colors')
    db_session.add(new_category)

    for item_name in default_items:
        new_item = Item(name=item_name, category=new_category)
        db_session.add(new_item)
    db_session.commit()


if __name__ == '__main__':
    print 'Creating database...'
    create_database()
    print 'Database created.'
    print 'Filling database with default data...'
    fill_default_data()
    print 'Default data added.'
