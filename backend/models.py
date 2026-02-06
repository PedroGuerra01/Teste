from sqlalchemy import Column, Integer, String, Float
from database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    empresa = Column(String, index=True)
    categoria = Column(String)
    tempo_resposta = Column(Float)
    satisfacao = Column(Integer)