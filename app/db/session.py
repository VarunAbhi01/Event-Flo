# SQLALCHEMY - is a python SQL toolkit and Object Relational Mapper (ORM) that allows python to interact with database. Database have tables and python have classes so instead of we writing all the SQL queires this will map the pythons classes and objects to the tables directly so we just by few lines of python can access and communicate with db.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# this is just a connection string to connect to the database named as eventflo
DATABASE_URL = "postgresql://localhost/eventflo"

# this will create a database connection to that eventflo db via the URL. echo is to log the sql queries in terminal for debugging purpose.
engine = create_engine(DATABASE_URL, echo=True)

# we cannot directly communicate with db after a connection is made instead, sessionmaker creates sessions say like workers or requests that communicates with db. And we will be calling this session local say like a machine that generates sessions via maker wherever needed in our entire app uniquely and we wont be using the same session for all the operations as that may lead to bugs.
# autoflush is to send the changes like insert/update to db without commiting them. so this autocommit and autoflush is to disable after each operation so that we can have control over when and what to push to db and commit.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# DB model is a python class that represents a table in the database. DdeclarativeBase is ORM engine that has all tables, columns, metadata mappping info. Its declared as base class for all the models to inherit from so that SQLAlchemy knows that these classes are special and should be treated as database tables.
# Base is the container or registry that collects all database models, and inheritance is how a class regsiters itself into that registry or tells SQLAlchemy “I am a table.” So SQLAlchemy can see all the tables defined under base adn create or manipulate them at once.
class Base(DeclarativeBase):
    pass