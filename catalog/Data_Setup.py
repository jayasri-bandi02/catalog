import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


# Set a Table for user with required columns
class GmailUser(Base):
    __tablename__ = 'gmailuser'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(220), nullable=False)


# Set a table to store item categories
class CategoryName(Base):
    __tablename__ = 'categoryname'
    id = Column(Integer, primary_key=True)
    name = Column(String(300), nullable=False)
    user_id = Column(Integer, ForeignKey('gmailuser.id'))
    user = relationship(GmailUser, backref="categoryname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


# Set a table to store item details
class ItemName(Base):
    __tablename__ = 'itemname1'
    id = Column(Integer, primary_key=True)
    itemname = Column(String(30), nullable=False)
    brand = Column(String(20))
    rating = Column(String(5))
    packing = Column(String(15))
    price = Column(String(10))
    date = Column(DateTime, nullable=False)
    categorynameid = Column(Integer, ForeignKey('categoryname.id'))
    categoryname = relationship(
        CategoryName, backref=backref('itemname', cascade='all, delete'))
    gmailuser_id = Column(Integer, ForeignKey('gmailuser.id'))
    gmailuser = relationship(GmailUser, backref="itemname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'itemname': self. itemname,
            'brand': self. brand,
            'rating': self. rating,
            'price': self. price,
            'packing': self. packing,
            'date': self. date,
            'id': self. id
        }


engine = create_engine('sqlite:///items.db')
Base.metadata.create_all(engine)
