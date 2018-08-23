import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    

class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return books category name and id in a JSON format"""
        return {
            'name': self.name,
            'id': self.id,
            }


class BookItem(Base):
    __tablename__ = 'book_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    book_id = Column(Integer, ForeignKey('book.id'))
    book = relationship(Book)

    @property
    def serialize(self):
        # Helps to return the data in JSON format
        return{
            'name' : self.name,
            'id' : self.id,
            'description' : self.description,
            'price' : self.price,
        }


engine = create_engine('sqlite:///bookitem.db')


Base.metadata.create_all(engine)