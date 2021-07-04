from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

User1 = User(name="System", email="system@example.com")
session.add(User1)
session.commit()

category1 = Category(user_id=1, name="Soccer")
session.add(category1)
session.commit()

item1cat1 = Item(user_id=1, title="Soccer Cleats",
                 description="The shoes", category=category1)
session.add(item1cat1)
session.commit()

item2cat1 = Item(user_id=1, title="Jersey",
                 description="The shirt", category=category1)
session.add(item2cat1)
session.commit()

category2 = Category(user_id=1, name="Basketball")
session.add(category2)
session.commit()

category3 = Category(user_id=1, name="Baseball")
session.add(category3)
session.commit()

item1cat3 = Item(user_id=1, title="Bat",
                 description="The bat", category=category3)
session.add(item1cat3)
session.commit()

category4 = Category(user_id=1, name="Frisbee")
session.add(category4)
session.commit()

category5 = Category(user_id=1, name="Snowboarding")
session.add(category5)
session.commit()

item1cat5 = Item(
    user_id=1,
    title="Snowboard",
    description="Best for any terrain and conditions",
    category=category5)
session.add(item1cat5)
session.commit()

print("filled database with items!")
