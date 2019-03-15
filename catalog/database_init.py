from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from Data_Setup import *

engine = create_engine('sqlite:///items.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
'''
 A DBSession() instance establishes all conversations with the database
 and represents a "staging zone" for all the objects loaded into the
 database session object. Any change made against the objects in the
 session won't be persisted into the database until you call
 session.commit(). If you're not happy about the changes, you can
 revert all of them back to the last commit by calling
 session.rollback()
'''
session = DBSession()

# Delete CategoryName if exisitng.
session.query(CategoryName).delete()
# Delete ItemName if exisitng.
session.query(ItemName).delete()
# Delete User if exisitng.
session.query(GmailUser).delete()

# Create sample users data
User1 = GmailUser(name="JayaSri Bandi",
                  email="bandijayasri02@gmail.com"
                  )
session.add(User1)
session.commit()
print ("Successfully Added  one user")
# Create sample categories
Category1 = CategoryName(name="Chocolate",
                         user_id=1)
session.add(Category1)
session.commit()

Category2 = CategoryName(name="Vanilla",
                         user_id=1)
session.add(Category2)
session.commit

Category3 = CategoryName(name="Fruits&Berry",
                         user_id=1)
session.add(Category3)
session.commit()

Category4 = CategoryName(name="NuttyCrunch",
                         user_id=1)
session.add(Category4)
session.commit()

Category5 = CategoryName(name="Exotic&Sundae",
                         user_id=1)
session.add(Category5)
session.commit()

# Show sample items in the categries added
Item1 = ItemName(itemname="Real Ice Cream - Choco Chips ",
                 brand="Amul",
                 rating="4.2",
                 price="Rs 156.75",
                 packing="1 lt Tub",
                 date=datetime.datetime.now(),
                       categorynameid=1,
                       gmailuser_id=1)
session.add(Item1)
session.commit()

Item2 = ItemName(itemname="Vanilla Magic",
                 brand="Amul",
                 rating="3.9",
                 price="Rs 123.75",
                 packing="1 lt Tub",
                 date=datetime.datetime.now(),
                 categorynameid=2,
                 gmailuser_id=1)
session.add(Item2)
session.commit()

Item3 = ItemName(itemname="Yoghurt Berry Delight",
                 brand="London Dairy",
                 rating="4.1",
                 price="Rs 300",
                 packing="500 ml Tub",
                 date=datetime.datetime.now(),
                 categorynameid=3,
                 gmailuser_id=1)
session.add(Item3)
session.commit()

Item4 = ItemName(itemname="Moroccan Dry Fruit",
                 brand="Amul",
                 rating="4.8",
                 price="Rs 181.50",
                 packing="1 lt Tub",
                 date=datetime.datetime.now(),
                 categorynameid=4,
                 gmailuser_id=1)
session.add(Item4)
session.commit()

Item5 = ItemName(itemname="Cotton Candy",
                 brand="Baskin Robbins",
                 rating="4.3",
                 price="Rs 183.20",
                 packing="500 ml Cup",
                 date=datetime.datetime.now(),
                 categorynameid=5,
                 gmailuser_id=1)
session.add(Item5)
session.commit()

# Message after all the data is inserted into database
print("Your items are inserted in the database !")
