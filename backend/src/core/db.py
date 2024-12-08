from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://SSS:SSS@localhost:5432/SSS")

Session = sessionmaker(bind=engine)
session = Session()
