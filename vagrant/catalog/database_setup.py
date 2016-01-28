import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'

    name = Column(String(80), nullable = False)
    address = Column(String(100), nullable = False)
    city = Column(String(50), nullable = False)
    state = Column(String(50), nullable = False)
    zip_code = Column(Integer, nullable = False)
    website = Column(String(250))
    id = Column(Integer, primary_key = True)

class Puppy(Base):
    __tablename__ = 'puppy'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    date_birth = Column(Date)
    gender = Column(String(10), nullable = False)
    weight = Column(Float, nullable = False)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))

    shelter = relationship(Shelter)
    

engine = create_engine('sqlite:///puppies.db')

Base.metadata.create_all(engine)
