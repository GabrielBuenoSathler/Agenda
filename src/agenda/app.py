from fastapi import FastAPI, Depends
from .schema import (
    CidadeSchema,
    CidadePublic

)
from .geo import get_coordinates
from .models  import Cidade
from sqlalchemy.orm import Session
from .database import get_session

from fastapi import HTTPException


app = FastAPI()


@app.get("/")
def root():
  return {"message": "Hello World"}

#@app.get("/lista_cidade" , responseModel=CidadePublic)
#def lista_cidade(Cidade: CidadeSchema, session: Session = Depends(get_session)):
#    pass

@app.post("/add_cidade" , response_model=CidadePublic)                             
def adiciona_cidade(cidade: CidadeSchema, session: Session = Depends(get_session)):
    #db_cidade = Cidade(cidade_nome =cidade.cidade_nome,lat = cidade.lat, long = cidade.long)
    print(cidade)
    latitute,longitude  = get_coordinates(cidade.cidade_nome)
    db_cidade = Cidade(cidade_nome=cidade.cidade_nome, lat=latitute, long=longitude) 
    session.add(db_cidade)                                                                                                  
    session.commit()                                                                                                      
    session.refresh(db_cidade)                                                                                              
    return db_cidade


@app.put("/up_cidade/{cidade_id}", response_model=CidadePublic)
def update_cidade(
    cidade_id: int,
    cidade: CidadeSchema,
    session: Session = Depends(get_session)
):
    db_cidade = session.get(Cidade, cidade_id)

    if not db_cidade:
        raise HTTPException(status_code=404, detail="Cidade não encontrada")

    db_cidade.cidade_nome = cidade.cidade_nome
    db_cidade.lat = cidade.lat
    db_cidade.long = cidade.long

    session.commit()
    session.refresh(db_cidade)

    return db_cidade


@app.delete("/del_cidade/{cidade_id}", response_model=CidadePublic)
def deleta_cidade(
    cidade_id: int,
    session: Session = Depends(get_session)
):
    db_cidade = session.get(Cidade, cidade_id)

    if not db_cidade:
        raise HTTPException(status_code=404, detail="Cidade não encontrada")

    session.delete(db_cidade)
    session.commit()

    return db_cidade
