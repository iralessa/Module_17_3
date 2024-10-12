# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, DeclarativeBase
# from sqlalchemy import Column,Integer, String
# engine = create_engine("sqlite:///ecommerce.db", echo=True)
#
# SessionLocal = sessionmaker(bind=engine)
#
# class Base(DeclarativeBase):
#     pass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column,Integer, String
engine = create_engine("sqlite:///taskmanager.db", echo=True)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
# class User(Base):
#     --tablename-- = "user"
#
#     id = Column(Integer,primary_key=True)
#     username = Column(String)
#     password = Column(String)

