from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#this url is used to create the location of the database on fastapi application.
'''this is for sqlite3'''
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

'''this is for postgresql'''
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Ukmh%400209@localhost/TodoApplicationDatabase'  

'''this is for mysql'''
#SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:Ukmh%400209@localhost/TodoApplicationDatabase'



#here the engine is created and passing args to tell like dont expect connection from single thread.
'''this is for sqlite3 database, the below one for postgresql'''
#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args= {'check_same_thread':False}) 
engine = create_engine(SQLALCHEMY_DATABASE_URL) 

#this helps the database fully, no autocommit, flash or nothing
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

#This base class allows you to define database tables as Python classes, making it easier to interact with the database using Python objects.
Base = declarative_base()