from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

## We want to load our environmental variables from dotenv file
load_dotenv()

## Getting our database url from our dotenv file
DATABASE_URL = os.getenv("DATABASE_URL")

## Create a database engine which is our connection to the postgreSQL database
database_engine = create_engine(DATABASE_URL)

## Each instance of the Sessionlocal class is a database session 

## Think of it as a doorway that opens each time you want to go into the database
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=database_engine)

Base = declarative_base()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()



