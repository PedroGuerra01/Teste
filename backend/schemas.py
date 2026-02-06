from pydantic import BaseModel

class TicketCreate(BaseModel):
    empresa: str
    categoria: str
    tempo_resposta: float
    satisfacao: int