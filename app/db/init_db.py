from app.db.session import engine
# although base is defined in sessions but all the tables are defined in models so we need to import base from models to have access to all the models defined there. once we import base form sesisons you have no models there so base has zero tbales registered, if its imported from models sqlalchemy makes usre that all models defined in that file are registered under base.
from app.db.models import Base

# metadata is all the information associated with the tables like their structure, relationships, columns, etc. create all creates all real SQL tables in database.
def init_db():
    Base.metadata.create_all(bind=engine)

# TThis makes sure only when this file is executed the init_db runs not every time it just gets imported somewhere else.
if __name__ == "__main__":
    init_db()