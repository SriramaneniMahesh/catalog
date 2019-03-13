import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)


class Bank_Name(Base):
    __tablename__ = 'bank_name'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="bank_name")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class Customer_Details(Base):
    __tablename__ = 'customer_details'
    id = Column(Integer, primary_key=True)
    cus_name = Column(String, nullable=False)
    acc_number = Column(String(150))
    cus_phone_number = Column(Integer)
    acc_type = Column(String, nullable=False)
    cus_address = Column(String(150), nullable=False)
    bank_name_id = Column(Integer, ForeignKey('bank_name.id'))
    bank_name = relationship(
        Bank_Name, backref=backref('customer_details', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="customer_details")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'cus_name': self. cus_name,
            'acc_number': self. acc_number,
            'cus_phone_number': self. cus_phone_number,
            'acc_type': self. acc_type,
            'cus_address': self. cus_address,
            'id': self. id
        }

eng = create_engine('sqlite:///bank_db.db')
Base.metadata.create_all(eng)
