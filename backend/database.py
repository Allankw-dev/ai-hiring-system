from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Create database engine
engine = create_engine("sqlite:///database.db")

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Create Candidate Table


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    match_score = Column(Float)
    experience = Column(Integer)


# Create the table in database
Base.metadata.create_all(engine)
