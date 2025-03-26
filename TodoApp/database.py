from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#this url is used to create the location of the database on fastapi application.
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'  

#here the engine is created and passing args to tell like dont expect connection from single thread.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args= {'check_same_thread':False}) 

#this helps the database fully, no autocommit, flash or nothing
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

#This base class allows you to define database tables as Python classes, making it easier to interact with the database using Python objects.
Base = declarative_base()