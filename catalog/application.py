from flask import Flask, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

app = Flask(__name__)

#Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#JSON APIs to retrieve all catalog items
@app.route('/catalog.json')
def catalogJSON():
    db_categories = session.query(Category).all()
    categories = []

    for c in db_categories:
        items = session.query(Item).filter_by(category_id = c.id).all()
        category = c.serialize

        if (len(items) > 0):
            category['Item'] = []

        for i in items:
            category['Item'].append(i.serialize)

        categories.append(category)

    return jsonify(Category = categories)

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)