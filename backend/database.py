from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(
    "sqlite:///habit.db",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    streak = Column(Integer, default=0)
    last_done = Column(Date, nullable=True)

Base.metadata.create_all(engine)
