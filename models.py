from sqlalchemy import Column, Float, Integer, String

from database import Base


class Memory(Base):
    __tablename__ = "memory"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    number_saved = Column(Float)


class ComplexMemory(Base):
    __tablename__ = "complex_memory"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cartesian = Column(String)
    real = Column(Float)
    imaginary = Column(Float)
    length = Column(Float)
