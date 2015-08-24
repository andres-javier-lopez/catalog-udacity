#coding: utf-8
"""Database definition."""

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
    items = orm.relationship('Item', backref="category",
                             order_by='Item.datetime.desc()')
    gplus_id = sqla.Column(sqla.String)

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': self.items
        }

class Item(Base):
    """Table that contains the items from the catalog.

    Atrributes:
        id: primary key of the item
        name: name of the item
    """

    __tablename__ = 'catalog'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(100), nullable=False)
    description = sqla.Column(sqla.String, default='')
    category_id = sqla.Column(sqla.ForeignKey('categories.id'), nullable=False)
    image = sqla.Column(sqla.String(100))
    datetime = sqla.Column(sqla.DateTime, default=sqla.func.now())
    gplus_id = sqla.Column(sqla.String)

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image':  self.image
        }


def parseJSON(o):
    """Parser for database objects.

    Convert database objects to a JSON version of them.

    Args:
        o: original object.

    Returns:
        JSON version of the object.

    Raises:
        TypeError: Raise an error if object cannot be converted.
    """
    if isinstance(o, Category) or isinstance(o, Item):
        return o.get_json()
    else:
        raise TypeError('object is not json serializable')


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

    default_items = ['Red', 'Blue', 'Black', 'Yellow', 'Green']
    new_category = Category(name='Colors')
    db_session.add(new_category)
    for item_name in default_items:
        description = '%s is a color' % item_name
        new_item = Item(name=item_name, description=description,
                        category=new_category)
        db_session.add(new_item)

    default_items = ['Apple', 'Strawberry', 'Watermelon', 'Orange']
    new_category = Category(name='Fruits')
    db_session.add(new_category)
    for item_name in default_items:
        description = '%s is a fruit' % item_name
        new_item = Item(name=item_name, description=description,
                        category=new_category)
        db_session.add(new_item)

    default_items = ['Dog', 'Cat', 'Horse', 'Cow']
    new_category = Category(name='Animals')
    db_session.add(new_category)
    for item_name in default_items:
        description = '%s is an animal' % item_name
        new_item = Item(name=item_name, description=description,
                        category=new_category)
        db_session.add(new_item)

    db_session.commit()


if __name__ == '__main__':
    print 'Creating database...'
    create_database()
    print 'Database created.'
    print 'Filling database with default data...'
    fill_default_data()
    print 'Default data added.'
