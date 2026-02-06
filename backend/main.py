from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Ticket
from schemas import TicketCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CX Dashboard - Vertem")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tickets")
def criar_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    novo = Ticket(**ticket.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@app.get("/insights/{empresa}")
def insights(empresa: str, db: Session = Depends(get_db)):
    tickets = db.query(Ticket).filter(Ticket.empresa == empresa).all()
    if not tickets:
        return {"mensagem": "Sem dados para esta empresa"}

    media_tempo = sum(t.tempo_resposta for t in tickets) / len(tickets)
    media_satisfacao = sum(t.satisfacao for t in tickets) / len(tickets)

    risco_churn = "ALTO" if media_satisfacao < 6 else "BAIXO"

    return {
        "empresa": empresa,
        "tempo_medio_resposta": round(media_tempo, 2),
        "satisfacao_media": round(media_satisfacao, 2),
        "risco_churn": risco_churn
    }